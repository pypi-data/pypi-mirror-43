import time
import uuid

from timeit import default_timer as timer

import boto3
import loguru
import spark_emr.bootstrap

from spark_optimizer.optimizer import (calculate_spark_settings,
                                       load_emr_instance)
from spark_emr.step import spark_step, spark_yarn_log_step
from spark_emr.util import S3Path

log = loguru.logger


class EmrManager(object):
    def __init__(self, config):
        self._config = config

        # instance configuration
        self._core_size_in_gb = config["core"]["size_in_gb"]
        self._core_type = config["core"]["instance_type"]
        self._master_type = config["master"]["instance_type"]
        self._master_size_in_gb = config["master"]["size_in_gb"]
        self._instance_count = config["core"]["instance_count"]
        self._ssh_key = config["ssh_key"]
        self._subnet_id = config["subnet_id"]
        self._optimization = config["optimization"]
        self._emr_version = config["emr_version"]
        self._consistent = config["consistent"]
        self._python_version = config["python_version"]
        self._bootstrap_uri = self.get_bootstrap_uri(
            config["bootstrap_uri"])
        self._region = config["region"]
        self._service_role = config["service_role"]
        self._job_flow_role = config["job_flow_role"]

        self.emr = boto3.client("emr", region_name=self._region)
        self.s3mgr = spark_emr.util.S3Manager(self._region)

        apps = ["Ganglia", "Spark", "Zeppelin"]
        self._apps_on_emr = [{"Name": app} for app in apps]

        # read remaining configuration
        self._log_uri = S3Path(self._bootstrap_uri).file_append("log").uri

        self.bm = spark_emr.bootstrap.BootstrapManager(
            self._region,
            self._python_version,
            self._bootstrap_uri
        )
        log.info("Used <<emr_config:%s>>" % self.__dict__)

    def get_bootstrap_uri(self, uri):
        uid = (uuid.uuid4()).hex
        return S3Path(uri).file_append(uid)

    def _create_classification_config(self):
        ret = [{
            "Classification": "spark",
            "Properties": {
                "maximizeResourceAllocation": "true",
            }
        }, {
            "Classification":
                "yarn-env",
            "Configurations": [{
                "Classification": "export",
                "Properties": {
                    "PYSPARK_PYTHON": self._python_version,
                    "PYSPARK_PYTHON_DRIVER": self._python_version
                }
            }]
        }, {
            "Classification": "core-site",
            "Properties": {
                "fs.s3a.endpoint": "s3.%s.amazonaws.com" % self._region
            }
        }, {
            "Classification": "emrfs-site",
            "Properties": {
                "fs.s3.consistent": "true" if self._consistent else "false",
            }
        }]

        if self._optimization:
            try:
                props, _ = calculate_spark_settings(self._core_type,
                                                    self._instance_count)
                props["spark.dynamicAllocation.enabled"] = "false"
                settings = {
                    "Classification": "spark-defaults",
                    "Properties": props
                }
                ret.append(settings)

                for x in ret:
                    if x["Classification"] == "spark":
                        x["Properties"]["maximizeResourceAllocation"] = "false"

            except Exception as e:
                log.warn("Unable to calculate <<spark_settings:%s>>" % e)

        log.info("Using EMR <<classification_config:%s>>" % ret)
        return ret

    def _create_instance_config(self, bid_master=None, bid_core=None):
        master = {
            "Name": "Master Instance",
            "InstanceRole": "MASTER",
            "InstanceType": self._master_type,
            "InstanceCount": 1,
            "EbsConfiguration": {
                    "EbsBlockDeviceConfigs": [
                        {
                            "VolumeSpecification": {
                                "VolumeType": "gp2",
                                "SizeInGB": self._master_size_in_gb
                            },
                            "VolumesPerInstance": 1
                        },
                    ],
                "EbsOptimized": True
            }
        }
        core = {
            "Name": "Core Instance",
            "InstanceRole": "CORE",
            "InstanceType": self._core_type,
            "InstanceCount": self._instance_count,
            "EbsConfiguration": {
                    "EbsBlockDeviceConfigs": [
                        {
                            "VolumeSpecification": {
                                "VolumeType": "gp2",
                                "SizeInGB": self._core_size_in_gb
                            },
                            "VolumesPerInstance": 1
                        },
                    ],
                "EbsOptimized": True
            }
        }
        if bid_master:
            master["BidPrice"] = str(bid_master)
            master["Market"] = "SPOT"
        if bid_core:
            core["BidPrice"] = str(bid_core)
            core["Market"] = "SPOT"
        ret = {
            "InstanceGroups": [master, core],
            "Ec2SubnetId": self._subnet_id,
            "Ec2KeyName": self._ssh_key,
            "KeepJobFlowAliveWhenNoSteps": True,
        }
        return ret

    def _launch(self,
                name,
                step=[],
                tag={},
                bootstrap_action=None,
                bid_master=None,
                bid_core=None):
        cluster_tag = []

        for k, v in tag.items():
            cluster_tag.append({"Key": k, "Value": v})

        job_flow_details = self.emr.run_job_flow(
            Name=name,
            Instances=self._create_instance_config(bid_master, bid_core),
            BootstrapActions=bootstrap_action,
            ServiceRole=self._service_role,
            ReleaseLabel=self._emr_version,
            Configurations=self._create_classification_config(),
            Applications=self._apps_on_emr,
            Steps=step,
            JobFlowRole=self._job_flow_role,
            LogUri=self._log_uri,
            VisibleToAllUsers=True,
            Tags=cluster_tag
        )
        self.job_flow_id = job_flow_details.get("JobFlowId")
        return self.job_flow_id

    def start(
            self,
            name,
            cmdline,
            package,
            tag,
            poll,
            yarn_log,
            bid_master,
            bid_core
    ):

        self.s3mgr.delete(self._bootstrap_uri.key, self._bootstrap_uri.bucket)

        bootstrap_action = self.bm.bootstrap(package)
        log.info(
            "Uploaded bootstrap <<bootstrap_uri:%s>>" % self._bootstrap_uri)
        cmd_step = spark_step(name,
                              cmdline,
                              self._python_version, "TERMINATE_JOB_FLOW")
        yarn_log_step = spark_yarn_log_step(self._bootstrap_uri, self._region)

        step = [cmd_step]

        if yarn_log:
            step.append(yarn_log_step)

        job_flow_id = self._launch(name, step, tag, bootstrap_action,
                                   bid_master, bid_core)
        self.bid_master = bid_master
        self.bid_core = bid_core

        log.info("EMR <<job_flow_id:%s>>" % job_flow_id)

        if poll:
            self.waiting()
            log.info("EMR <<job_flow_id_finished:%s>>" % job_flow_id)
        return job_flow_id

    def add_steps(self, steps):
        return self.emr.add_job_flow_steps(
            JobFlowId=self.job_flow_id, Steps=steps)

    def status(self):
        return status(self.job_flow_id)

    def stop(self):
        return stop([self.job_flow_id], self._region)

    def _log_cost(self):
        try:
            config = load_emr_instance()
            master_info = config[self._master_type]["pricing"]
            core_info = config[self._core_type]["pricing"]
            ec2_master = float(master_info[self._region]["ec2"])
            if self.bid_master:
                ec2_master = self.bid_master 
            ec2_core = float(core_info[self._region]["ec2"])
            if self.bid_core:
                ec2_core = self.bid_core 
            mcost = (ec2_master + float(master_info[self._region]["emr"]))
            ccost = ((ec2_core + float(core_info[self._region]["emr"])) *
                     self._instance_count)
            cost_per_hour = mcost + ccost
            end = timer()
            # uptime is in seconds
            uptime = end - self._start_timer
            cost_since = (cost_per_hour / 3600) * uptime
            log.info("Approximate <<cost:%.4f$>> <<uptime:%.2fm>>" %
                     (cost_since, (uptime / 60)))
        except Exception:
            pass

    def waiting(self, polling_interval=10):
        self._start_timer = timer()
        while True:
            keep_waiting = self._step_finished()
            self._log_cost()
            if not keep_waiting:
                break
            time.sleep(polling_interval)

        self.stop()

    def _step_finished(self):
        JOB_STATES = ["TERMINATED", "COMPLETED", "FAILED"]
        all_steps = self.emr.list_steps(
            ClusterId=self.job_flow_id)["Steps"]
        completed = [
            step["Status"]["State"] in JOB_STATES for step in all_steps
        ]
        finished = sum(completed)
        log.info(
            "Total <<job_number:%s>> are <<finished:%s>> with "
            "<<job_flow_id:%s>>" %
            (len(completed), finished, self.job_flow_id))
        return not all(completed)


def status(job_flow_id, region):
    emr = boto3.client("emr", region_name=region)
    return emr.describe_cluster(ClusterId=job_flow_id)


def stop(job_flow_ids, region):
    emr = boto3.client("emr", region_name=region)
    return emr.terminate_job_flows(JobFlowIds=job_flow_ids)


def list(_filter, region):
    emr = boto3.client("emr", region_name=region)
    ret = []

    def comp(x, y):
        return {k: x[k] for k in x if k in y and x[k] == y[k]}

    def _collect(page):
        for p in page:
            cluster = status(p["Id"], region)["Cluster"]
            tag = {x["Key"]: x["Value"] for x in cluster["Tags"]}
            cluster["TagsClean"] = tag

            if _filter and len(comp(_filter, tag)) == len(_filter):
                continue
            ret.append(cluster)

    page = emr.list_clusters()
    _collect(page["Clusters"])
    while page.get("Marker"):
        page = emr.list_clusters(Marker=page["Marker"])
        _collect(page["Clusters"])

    return ret
