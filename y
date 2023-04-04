version = 0.1
[y]
[y.deploy]
[y.deploy.parameters]
stack_name = "HttpAPItest"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-1e1b8ujnt4wl6"
s3_prefix = "HttpAPItest"
region = "us-west-2"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
parameter_overrides = "AppName=\"student-app\" ClientDomains=\"localhost\" StudentEmail=\"kibria.papel@gmail.com\" AddGroupsToScopes=\"true\""
