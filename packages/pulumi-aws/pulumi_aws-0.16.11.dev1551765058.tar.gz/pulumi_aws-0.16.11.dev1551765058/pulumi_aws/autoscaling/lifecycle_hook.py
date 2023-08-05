# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class LifecycleHook(pulumi.CustomResource):
    autoscaling_group_name: pulumi.Output[str]
    """
    The name of the Auto Scaling group to which you want to assign the lifecycle hook
    """
    default_result: pulumi.Output[str]
    """
    Defines the action the Auto Scaling group should take when the lifecycle hook timeout elapses or if an unexpected failure occurs. The value for this parameter can be either CONTINUE or ABANDON. The default value for this parameter is ABANDON.
    """
    heartbeat_timeout: pulumi.Output[int]
    """
    Defines the amount of time, in seconds, that can elapse before the lifecycle hook times out. When the lifecycle hook times out, Auto Scaling performs the action defined in the DefaultResult parameter
    """
    lifecycle_transition: pulumi.Output[str]
    """
    The instance state to which you want to attach the lifecycle hook. For a list of lifecycle hook types, see [describe-lifecycle-hook-types](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/describe-lifecycle-hook-types.html#examples)
    """
    name: pulumi.Output[str]
    """
    The name of the lifecycle hook.
    """
    notification_metadata: pulumi.Output[str]
    """
    Contains additional information that you want to include any time Auto Scaling sends a message to the notification target.
    """
    notification_target_arn: pulumi.Output[str]
    """
    The ARN of the notification target that Auto Scaling will use to notify you when an instance is in the transition state for the lifecycle hook. This ARN target can be either an SQS queue or an SNS topic.
    """
    role_arn: pulumi.Output[str]
    """
    The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target.
    """
    def __init__(__self__, resource_name, opts=None, autoscaling_group_name=None, default_result=None, heartbeat_timeout=None, lifecycle_transition=None, name=None, notification_metadata=None, notification_target_arn=None, role_arn=None, __name__=None, __opts__=None):
        """
        Provides an AutoScaling Lifecycle Hook resource.
        
        > **NOTE:** Terraform has two types of ways you can add lifecycle hooks - via
        the `initial_lifecycle_hook` attribute from the
        [`aws_autoscaling_group`](https://www.terraform.io/docs/providers/aws/r/autoscaling_group.html)
        resource, or via this one. Hooks added via this resource will not be added
        until the autoscaling group has been created, and depending on your
        [capacity](https://www.terraform.io/docs/providers/aws/r/autoscaling_group.html#waiting-for-capacity)
        settings, after the initial instances have been launched, creating unintended
        behavior. If you need hooks to run on all instances, add them with
        `initial_lifecycle_hook` in
        [`aws_autoscaling_group`](https://www.terraform.io/docs/providers/aws/r/autoscaling_group.html),
        but take care to not duplicate those hooks with this resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] autoscaling_group_name: The name of the Auto Scaling group to which you want to assign the lifecycle hook
        :param pulumi.Input[str] default_result: Defines the action the Auto Scaling group should take when the lifecycle hook timeout elapses or if an unexpected failure occurs. The value for this parameter can be either CONTINUE or ABANDON. The default value for this parameter is ABANDON.
        :param pulumi.Input[int] heartbeat_timeout: Defines the amount of time, in seconds, that can elapse before the lifecycle hook times out. When the lifecycle hook times out, Auto Scaling performs the action defined in the DefaultResult parameter
        :param pulumi.Input[str] lifecycle_transition: The instance state to which you want to attach the lifecycle hook. For a list of lifecycle hook types, see [describe-lifecycle-hook-types](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/describe-lifecycle-hook-types.html#examples)
        :param pulumi.Input[str] name: The name of the lifecycle hook.
        :param pulumi.Input[str] notification_metadata: Contains additional information that you want to include any time Auto Scaling sends a message to the notification target.
        :param pulumi.Input[str] notification_target_arn: The ARN of the notification target that Auto Scaling will use to notify you when an instance is in the transition state for the lifecycle hook. This ARN target can be either an SQS queue or an SNS topic.
        :param pulumi.Input[str] role_arn: The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if autoscaling_group_name is None:
            raise TypeError('Missing required property autoscaling_group_name')
        __props__['autoscaling_group_name'] = autoscaling_group_name

        __props__['default_result'] = default_result

        __props__['heartbeat_timeout'] = heartbeat_timeout

        if lifecycle_transition is None:
            raise TypeError('Missing required property lifecycle_transition')
        __props__['lifecycle_transition'] = lifecycle_transition

        __props__['name'] = name

        __props__['notification_metadata'] = notification_metadata

        __props__['notification_target_arn'] = notification_target_arn

        __props__['role_arn'] = role_arn

        super(LifecycleHook, __self__).__init__(
            'aws:autoscaling/lifecycleHook:LifecycleHook',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

