import json
import pulumi_aws as aws
import configparser

# CONFIG
CONFIG_FILE='dwh.cfg'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

DB_NAME=config.get("CLUSTER","DB_NAME")
DB_USER=config.get("CLUSTER","DB_USER")
DB_PASSWORD=config.get("CLUSTER","DB_PASSWORD")
DB_PORT=config.get("CLUSTER","DB_PORT")
IAM_NAME = config.get("IAM_ROLE","NAME")


redshift_role = aws.iam.Role(IAM_NAME,
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Sid": "",
            "Principal": {
                "Service": "redshift.amazonaws.com",
            },
        }],
    }))


redshift_cluster = aws.redshift.Cluster("default",
    cluster_identifier="moshe-cluster",
    cluster_type="single-node",
    database_name=DB_NAME,
    master_password=DB_PASSWORD,
    master_username=DB_PASSWORD,
    node_type="dc1.large",
    iam_roles=[redshift_role],
    port=DB_PORT)

config.set('IAM_ROLE', 'ARN', str(redshift_role))
config.set('CLUSTER', 'HOST', str(redshift_cluster))

with open("CONFIG_FILE.ini", "w+") as configfile:
    config.write(configfile)