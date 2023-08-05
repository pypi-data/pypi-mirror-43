# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Policy(pulumi.CustomResource):
    adjustment_type: pulumi.Output[str]
    """
    The scaling policy's adjustment type.
    """
    alarms: pulumi.Output[list]
    arn: pulumi.Output[str]
    """
    The ARN assigned by AWS to the scaling policy.
    """
    cooldown: pulumi.Output[int]
    metric_aggregation_type: pulumi.Output[str]
    min_adjustment_magnitude: pulumi.Output[int]
    name: pulumi.Output[str]
    """
    The name of the policy.
    """
    policy_type: pulumi.Output[str]
    """
    For DynamoDB, only `TargetTrackingScaling` is supported. For Amazon ECS, Spot Fleet, and Amazon RDS, both `StepScaling` and `TargetTrackingScaling` are supported. For any other service, only `StepScaling` is supported. Defaults to `StepScaling`.
    """
    resource_id: pulumi.Output[str]
    """
    The resource type and unique identifier string for the resource associated with the scaling policy. Documentation can be found in the `ResourceId` parameter at: [AWS Application Auto Scaling API Reference](http://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestParameters)
    """
    scalable_dimension: pulumi.Output[str]
    """
    The scalable dimension of the scalable target. Documentation can be found in the `ScalableDimension` parameter at: [AWS Application Auto Scaling API Reference](http://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestParameters)
    """
    service_namespace: pulumi.Output[str]
    """
    The AWS service namespace of the scalable target. Documentation can be found in the `ServiceNamespace` parameter at: [AWS Application Auto Scaling API Reference](http://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestParameters)
    """
    step_adjustments: pulumi.Output[list]
    step_scaling_policy_configurations: pulumi.Output[list]
    """
    Step scaling policy configuration, requires `policy_type = "StepScaling"` (default). See supported fields below.
    """
    target_tracking_scaling_policy_configuration: pulumi.Output[dict]
    """
    A target tracking policy, requires `policy_type = "TargetTrackingScaling"`. See supported fields below.
    """
    def __init__(__self__, resource_name, opts=None, adjustment_type=None, alarms=None, cooldown=None, metric_aggregation_type=None, min_adjustment_magnitude=None, name=None, policy_type=None, resource_id=None, scalable_dimension=None, service_namespace=None, step_adjustments=None, step_scaling_policy_configurations=None, target_tracking_scaling_policy_configuration=None, __name__=None, __opts__=None):
        """
        Provides an Application AutoScaling Policy resource.
        
        ## Nested fields
        
        ### `target_tracking_scaling_policy_configuration`
        
        * `target_value` - (Required) The target value for the metric.
        * `disable_scale_in` - (Optional) Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. The default value is `false`.
        * `scale_in_cooldown` - (Optional) The amount of time, in seconds, after a scale in activity completes before another scale in activity can start.
        * `scale_out_cooldown` - (Optional) The amount of time, in seconds, after a scale out activity completes before another scale out activity can start.
        * `customized_metric_specification` - (Optional) Reserved for future use. See supported fields below.
        * `predefined_metric_specification` - (Optional) A predefined metric. See supported fields below.
        
        ### `customized_metric_specification`
        
        * `dimensions` - (Optional) The dimensions of the metric.
        * `metric_name` - (Required) The name of the metric.
        * `namespace` - (Required) The namespace of the metric.
        * `statistic` - (Required) The statistic of the metric.
        * `unit` - (Optional) The unit of the metric.
        
        ### `predefined_metric_specification`
        
        * `predefined_metric_type` - (Required) The metric type.
        * `resource_label` - (Optional) Reserved for future use.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] adjustment_type: The scaling policy's adjustment type.
        :param pulumi.Input[str] name: The name of the policy.
        :param pulumi.Input[str] policy_type: For DynamoDB, only `TargetTrackingScaling` is supported. For Amazon ECS, Spot Fleet, and Amazon RDS, both `StepScaling` and `TargetTrackingScaling` are supported. For any other service, only `StepScaling` is supported. Defaults to `StepScaling`.
        :param pulumi.Input[str] resource_id: The resource type and unique identifier string for the resource associated with the scaling policy. Documentation can be found in the `ResourceId` parameter at: [AWS Application Auto Scaling API Reference](http://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestParameters)
        :param pulumi.Input[str] scalable_dimension: The scalable dimension of the scalable target. Documentation can be found in the `ScalableDimension` parameter at: [AWS Application Auto Scaling API Reference](http://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestParameters)
        :param pulumi.Input[str] service_namespace: The AWS service namespace of the scalable target. Documentation can be found in the `ServiceNamespace` parameter at: [AWS Application Auto Scaling API Reference](http://docs.aws.amazon.com/ApplicationAutoScaling/latest/APIReference/API_RegisterScalableTarget.html#API_RegisterScalableTarget_RequestParameters)
        :param pulumi.Input[list] step_scaling_policy_configurations: Step scaling policy configuration, requires `policy_type = "StepScaling"` (default). See supported fields below.
        :param pulumi.Input[dict] target_tracking_scaling_policy_configuration: A target tracking policy, requires `policy_type = "TargetTrackingScaling"`. See supported fields below.
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

        __props__['adjustment_type'] = adjustment_type

        __props__['alarms'] = alarms

        __props__['cooldown'] = cooldown

        __props__['metric_aggregation_type'] = metric_aggregation_type

        __props__['min_adjustment_magnitude'] = min_adjustment_magnitude

        __props__['name'] = name

        __props__['policy_type'] = policy_type

        if resource_id is None:
            raise TypeError('Missing required property resource_id')
        __props__['resource_id'] = resource_id

        if scalable_dimension is None:
            raise TypeError('Missing required property scalable_dimension')
        __props__['scalable_dimension'] = scalable_dimension

        if service_namespace is None:
            raise TypeError('Missing required property service_namespace')
        __props__['service_namespace'] = service_namespace

        __props__['step_adjustments'] = step_adjustments

        __props__['step_scaling_policy_configurations'] = step_scaling_policy_configurations

        __props__['target_tracking_scaling_policy_configuration'] = target_tracking_scaling_policy_configuration

        __props__['arn'] = None

        super(Policy, __self__).__init__(
            'aws:appautoscaling/policy:Policy',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

