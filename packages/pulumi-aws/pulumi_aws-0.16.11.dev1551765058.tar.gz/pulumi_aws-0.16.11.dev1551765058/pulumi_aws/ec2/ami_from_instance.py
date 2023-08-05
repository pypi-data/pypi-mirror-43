# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class AmiFromInstance(pulumi.CustomResource):
    architecture: pulumi.Output[str]
    """
    Machine architecture for created instances. Defaults to "x86_64".
    """
    description: pulumi.Output[str]
    """
    A longer, human-readable description for the AMI.
    """
    ebs_block_devices: pulumi.Output[list]
    """
    Nested block describing an EBS block device that should be
    attached to created instances. The structure of this block is described below.
    """
    ena_support: pulumi.Output[bool]
    """
    Specifies whether enhanced networking with ENA is enabled. Defaults to `false`.
    """
    ephemeral_block_devices: pulumi.Output[list]
    """
    Nested block describing an ephemeral block device that
    should be attached to created instances. The structure of this block is described below.
    """
    image_location: pulumi.Output[str]
    """
    Path to an S3 object containing an image manifest, e.g. created
    by the `ec2-upload-bundle` command in the EC2 command line tools.
    """
    kernel_id: pulumi.Output[str]
    """
    The id of the kernel image (AKI) that will be used as the paravirtual
    kernel in created instances.
    """
    manage_ebs_snapshots: pulumi.Output[bool]
    name: pulumi.Output[str]
    """
    A region-unique name for the AMI.
    """
    ramdisk_id: pulumi.Output[str]
    """
    The id of an initrd image (ARI) that will be used when booting the
    created instances.
    """
    root_device_name: pulumi.Output[str]
    """
    The name of the root device (for example, `/dev/sda1`, or `/dev/xvda`).
    """
    root_snapshot_id: pulumi.Output[str]
    snapshot_without_reboot: pulumi.Output[bool]
    """
    Boolean that overrides the behavior of stopping
    the instance before snapshotting. This is risky since it may cause a snapshot of an
    inconsistent filesystem state, but can be used to avoid downtime if the user otherwise
    guarantees that no filesystem writes will be underway at the time of snapshot.
    """
    source_instance_id: pulumi.Output[str]
    """
    The id of the instance to use as the basis of the AMI.
    """
    sriov_net_support: pulumi.Output[str]
    """
    When set to "simple" (the default), enables enhanced networking
    for created instances. No other value is supported at this time.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    virtualization_type: pulumi.Output[str]
    """
    Keyword to choose what virtualization mode created instances
    will use. Can be either "paravirtual" (the default) or "hvm". The choice of virtualization type
    changes the set of further arguments that are required, as described below.
    """
    def __init__(__self__, resource_name, opts=None, description=None, ebs_block_devices=None, ephemeral_block_devices=None, name=None, snapshot_without_reboot=None, source_instance_id=None, tags=None, __name__=None, __opts__=None):
        """
        The "AMI from instance" resource allows the creation of an Amazon Machine
        Image (AMI) modelled after an existing EBS-backed EC2 instance.
        
        The created AMI will refer to implicitly-created snapshots of the instance's
        EBS volumes and mimick its assigned block device configuration at the time
        the resource is created.
        
        This resource is best applied to an instance that is stopped when this instance
        is created, so that the contents of the created image are predictable. When
        applied to an instance that is running, *the instance will be stopped before taking
        the snapshots and then started back up again*, resulting in a period of
        downtime.
        
        Note that the source instance is inspected only at the initial creation of this
        resource. Ongoing updates to the referenced instance will not be propagated into
        the generated AMI. Users may taint or otherwise recreate the resource in order
        to produce a fresh snapshot.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A longer, human-readable description for the AMI.
        :param pulumi.Input[list] ebs_block_devices: Nested block describing an EBS block device that should be
               attached to created instances. The structure of this block is described below.
        :param pulumi.Input[list] ephemeral_block_devices: Nested block describing an ephemeral block device that
               should be attached to created instances. The structure of this block is described below.
        :param pulumi.Input[str] name: A region-unique name for the AMI.
        :param pulumi.Input[bool] snapshot_without_reboot: Boolean that overrides the behavior of stopping
               the instance before snapshotting. This is risky since it may cause a snapshot of an
               inconsistent filesystem state, but can be used to avoid downtime if the user otherwise
               guarantees that no filesystem writes will be underway at the time of snapshot.
        :param pulumi.Input[str] source_instance_id: The id of the instance to use as the basis of the AMI.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
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

        __props__['description'] = description

        __props__['ebs_block_devices'] = ebs_block_devices

        __props__['ephemeral_block_devices'] = ephemeral_block_devices

        __props__['name'] = name

        __props__['snapshot_without_reboot'] = snapshot_without_reboot

        if source_instance_id is None:
            raise TypeError('Missing required property source_instance_id')
        __props__['source_instance_id'] = source_instance_id

        __props__['tags'] = tags

        __props__['architecture'] = None
        __props__['ena_support'] = None
        __props__['image_location'] = None
        __props__['kernel_id'] = None
        __props__['manage_ebs_snapshots'] = None
        __props__['ramdisk_id'] = None
        __props__['root_device_name'] = None
        __props__['root_snapshot_id'] = None
        __props__['sriov_net_support'] = None
        __props__['virtualization_type'] = None

        super(AmiFromInstance, __self__).__init__(
            'aws:ec2/amiFromInstance:AmiFromInstance',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

