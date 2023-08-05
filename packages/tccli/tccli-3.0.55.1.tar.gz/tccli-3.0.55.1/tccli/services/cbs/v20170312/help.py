# -*- coding: utf-8 -*-
DESC = "cbs-2017-03-12"
INFO = {
  "CreateDisks": {
    "params": [
      {
        "name": "DiskType",
        "desc": "硬盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬盘<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。"
      },
      {
        "name": "DiskChargeType",
        "desc": "云硬盘计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费<br>各类型价格请参考云硬盘[价格总览](/document/product/362/2413)。"
      },
      {
        "name": "Placement",
        "desc": "实例所在的位置。通过该参数可以指定实例所属可用区，所属项目。若不指定项目，将在默认项目下进行创建。"
      },
      {
        "name": "DiskName",
        "desc": "云盘显示名称。不传则默认为“未命名”。最大长度不能超60个字节。"
      },
      {
        "name": "DiskCount",
        "desc": "创建云硬盘数量，不传则默认为1。单次请求最多可创建的云盘数有限制，具体参见[云硬盘使用限制](https://cloud.tencent.com/doc/product/362/5145)。"
      },
      {
        "name": "DiskChargePrepaid",
        "desc": "预付费模式，即包年包月相关参数设置。通过该参数指定包年包月云盘的购买时长、是否设置自动续费等属性。<br>创建预付费云盘该参数必传，创建按小时后付费云盘无需传该参数。"
      },
      {
        "name": "DiskSize",
        "desc": "云硬盘大小，单位为GB。<br><li>如果传入`SnapshotId`则可不传`DiskSize`，此时新建云盘的大小为快照大小<br><li>如果传入`SnapshotId`同时传入`DiskSize`，则云盘大小必须大于或等于快照大小<br><li>云盘大小取值范围参见云硬盘[产品分类](/document/product/362/2353)的说明。"
      },
      {
        "name": "SnapshotId",
        "desc": "快照ID，如果传入则根据此快照创建云硬盘，快照类型必须为数据盘快照，可通过[DescribeSnapshots](/document/product/362/15647)接口查询快照，见输出参数DiskUsage解释。"
      },
      {
        "name": "ClientToken",
        "desc": "用于保证请求幂等性的字符串。该字符串由客户生成，需保证不同请求之间唯一，最大值不超过64个ASCII字符。若不指定该参数，则无法保证请求的幂等性。"
      },
      {
        "name": "Encrypt",
        "desc": "传入该参数用于创建加密云盘，取值固定为ENCRYPT。"
      },
      {
        "name": "Tags",
        "desc": "云盘绑定的标签。"
      },
      {
        "name": "DeleteWithInstance",
        "desc": "可选参数，不传该参数则仅执行挂载操作。传入True时，新创建的云盘将设置为随云主机销毁模式，仅对按量计费云硬盘有效。"
      }
    ],
    "desc": "本接口（CreateDisks）用于创建云硬盘。\n\n* 预付费云盘的购买会预先扣除本次云盘购买所需金额，在调用本接口前请确保账户余额充足。\n* 本接口支持传入数据盘快照来创建云盘，实现将快照数据复制到新购云盘上。\n* 本接口为异步接口，当创建请求下发成功后会返回一个新建的云盘ID列表，此时云盘的创建并未立即完成。可以通过调用[DescribeDisks](/document/product/362/16315)接口根据DiskId查询对应云盘，如果能查到云盘，且状态为'UNATTACHED'或'ATTACHED'，则表示创建成功。"
  },
  "InquiryPriceRenewDisks": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "云硬盘ID， 通过[DescribeDisks](/document/product/362/16315)接口查询。"
      },
      {
        "name": "DiskChargePrepaids",
        "desc": "预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的购买时长。如果在该参数中指定CurInstanceDeadline，则会按对齐到子机到期时间来续费。如果是批量续费询价，该参数与Disks参数一一对应，元素数量需保持一致。"
      },
      {
        "name": "NewDeadline",
        "desc": "指定云盘新的到期时间，形式如：2017-12-17 00:00:00。参数`NewDeadline`和`DiskChargePrepaids`是两种指定询价时长的方式，两者必传一个。"
      },
      {
        "name": "ProjectId",
        "desc": "云盘所属项目ID。 如传入则仅用于鉴权。"
      }
    ],
    "desc": "本接口（InquiryPriceRenewDisks）用于续费云硬盘询价。\n\n* 只支持查询预付费模式的弹性云盘续费价格。\n* 支持与挂载实例一起续费的场景，需要在[DiskChargePrepaid](/document/product/362/15669#DiskChargePrepaid)参数中指定CurInstanceDeadline，此时会按对齐到实例续费后的到期时间来续费询价。\n* 支持为多块云盘指定不同的续费时长，此时返回的价格为多块云盘续费的总价格。"
  },
  "InquiryPriceResizeDisk": {
    "params": [
      {
        "name": "DiskId",
        "desc": "云硬盘ID， 通过[DescribeDisks](/document/product/362/16315)接口查询。"
      },
      {
        "name": "DiskSize",
        "desc": "云硬盘扩容后的大小，单位为GB，不得小于当前云硬盘大小。云盘大小取值范围参见云硬盘[产品分类](/document/product/362/2353)的说明。"
      },
      {
        "name": "ProjectId",
        "desc": "云盘所属项目ID。 如传入则仅用于鉴权。"
      }
    ],
    "desc": "本接口（InquiryPriceResizeDisk）用于扩容云硬盘询价。\n\n* 只支持预付费模式的云硬盘扩容询价。"
  },
  "RenewDisk": {
    "params": [
      {
        "name": "DiskChargePrepaid",
        "desc": "预付费模式，即包年包月相关参数设置。通过该参数可以指定包年包月云盘的续费时长。<br>在云盘与挂载的实例一起续费的场景下，可以指定参数CurInstanceDeadline，此时云盘会按对齐到实例续费后的到期时间来续费。"
      },
      {
        "name": "DiskId",
        "desc": "云硬盘ID， 通过[DescribeDisks](/document/product/362/16315)接口查询。"
      }
    ],
    "desc": "本接口（RenewDisk）用于续费云硬盘。\n\n* 只支持预付费的云硬盘。云硬盘类型可以通过[DescribeDisks](/document/product/362/16315)接口查询，见输出参数中DiskChargeType字段解释。\n* 支持与挂载实例一起续费的场景，需要在[DiskChargePrepaid](/document/product/362/15669#DiskChargePrepaid)参数中指定CurInstanceDeadline，此时会按对齐到子机续费后的到期时间来续费。"
  },
  "ModifyDiskAttributes": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "一个或多个待操作的云硬盘ID。如果传入多个云盘ID，仅支持所有云盘修改为同一属性。"
      },
      {
        "name": "ProjectId",
        "desc": "新的云硬盘项目ID，只支持修改弹性云盘的项目ID。通过[DescribeProject](/document/api/378/4400)接口查询可用项目及其ID。"
      },
      {
        "name": "DiskName",
        "desc": "新的云硬盘名称。"
      },
      {
        "name": "Portable",
        "desc": "是否为弹性云盘，FALSE表示非弹性云盘，TRUE表示弹性云盘。仅支持非弹性云盘修改为弹性云盘。"
      },
      {
        "name": "DeleteWithInstance",
        "desc": "成功挂载到云主机后该云硬盘是否随云主机销毁，TRUE表示随云主机销毁，FALSE表示不随云主机销毁。仅支持按量计费云硬盘数据盘。"
      },
      {
        "name": "DiskType",
        "desc": "变更云盘类型时，可传入该参数，表示变更的目标类型，取值范围：<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。<br>当前不支持批量变更类型，即传入DiskType时，DiskIds仅支持传入一块云盘；<br>变更云盘类型时不支持同时变更其他属性。"
      }
    ],
    "desc": "* 只支持修改弹性云盘的项目ID。随云主机创建的云硬盘项目ID与云主机联动。可以通过[DescribeDisks](/document/product/362/16315)接口查询，见输出参数中Portable字段解释。\n* “云硬盘名称”仅为方便用户自己管理之用，腾讯云并不以此名称作为提交工单或是进行云盘管理操作的依据。\n* 支持批量操作，如果传入多个云盘ID，则所有云盘修改为同一属性。如果存在不允许操作的云盘，则操作不执行，以特定错误码返回。\n* 支持修改弹性云盘的云盘类型，不支持非弹性云盘（[DescribeDisks](/document/product/362/16315)接口的返回字段Portable为true表示弹性云盘），且当前仅支持云盘类型升级，不支持降级，具体如下:\n    * CLOUD_BASIC变更为CLOUD_PREMIUM；\n    * CLOUD_BASIC变更为CLOUD_SSD；\n    * CLOUD_PREMIUM变更为CLOUD_SSD。\n* 云盘处于“迁移中”不影响正常的读写以及读写速率，在云盘容量较大的情况下，整个迁移任务耗时较长，目前不支持任务成功发起后取消任务。"
  },
  "DeleteSnapshots": {
    "params": [
      {
        "name": "SnapshotIds",
        "desc": "要删除的快照ID列表，可通过[DescribeSnapshots](/document/product/362/15647)查询。"
      }
    ],
    "desc": "本接口（DeleteSnapshots）用于删除快照。\n\n* 快照必须处于NORMAL状态，快照状态可以通过[DescribeSnapshots](/document/product/362/15647)接口查询，见输出参数中SnapshotState字段解释。\n* 支持批量操作。如果多个快照存在无法删除的快照，则操作不执行，以返回特定的错误码返回。"
  },
  "DescribeInstancesDiskNum": {
    "params": [
      {
        "name": "InstanceIds",
        "desc": "云服务器实例ID，通过[DescribeInstances](/document/product/213/15728)接口查询。"
      }
    ],
    "desc": "本接口（DescribeInstancesDiskNum）用于查询实例已挂载云硬盘数量。\n\n* 支持批量操作，当传入多个云服务器实例ID，返回结果会分别列出每个云服务器挂载的云硬盘数量。"
  },
  "InquiryPriceCreateDisks": {
    "params": [
      {
        "name": "DiskType",
        "desc": "云硬盘类型。取值范围：<br><li>普通云硬盘：CLOUD_BASIC<br><li>高性能云硬盘：CLOUD_PREMIUM<br><li>SSD云硬盘：CLOUD_SSD。"
      },
      {
        "name": "DiskSize",
        "desc": "云硬盘大小，单位为GB。云盘大小取值范围参见云硬盘[产品分类](/document/product/362/2353)的说明。"
      },
      {
        "name": "DiskChargeType",
        "desc": "云硬盘计费类型。<br><li>PREPAID：预付费，即包年包月<br><li>POSTPAID_BY_HOUR：按小时后付费"
      },
      {
        "name": "DiskChargePrepaid",
        "desc": "预付费模式，即包年包月相关参数设置。通过该参数指定包年包月云盘的购买时长、是否设置自动续费等属性。<br>创建预付费云盘该参数必传，创建按小时后付费云盘无需传该参数。"
      },
      {
        "name": "DiskCount",
        "desc": "购买云盘的数量。不填则默认为1。"
      },
      {
        "name": "ProjectId",
        "desc": "云盘所属项目ID。"
      }
    ],
    "desc": "本接口（InquiryPriceCreateDisks）用于创建云硬盘询价。\n\n* 支持查询创建多块云硬盘的价格，此时返回结果为总价格。"
  },
  "ApplySnapshot": {
    "params": [
      {
        "name": "SnapshotId",
        "desc": "快照ID, 可通过[DescribeSnapshots](/document/product/362/15647)查询。"
      },
      {
        "name": "DiskId",
        "desc": "快照原云硬盘ID，可通过[DescribeDisks](/document/product/362/16315)接口查询。"
      }
    ],
    "desc": "本接口（ApplySnapshot）用于回滚快照到原云硬盘。\n\n* 仅支持回滚到原云硬盘上。对于数据盘快照，如果您需要复制快照数据到其它云硬盘上，请使用[CreateDisks](/document/product/362/16312)接口创建新的弹性云盘，将快照数据复制到新购云盘上。 \n* 用于回滚的快照必须处于NORMAL状态。快照状态可以通过[DescribeSnapshots](/document/product/362/15647)接口查询，见输出参数中SnapshotState字段解释。\n* 如果是弹性云盘，则云盘必须处于未挂载状态，云硬盘挂载状态可以通过[DescribeDisks](/document/product/362/16315)接口查询，见Attached字段解释；如果是随实例一起购买的非弹性云盘，则实例必须处于关机状态，实例状态可以通过[DescribeInstancesStatus](/document/product/213/15738)接口查询。"
  },
  "DescribeSnapshotOperationLogs": {
    "params": [
      {
        "name": "Filters",
        "desc": "过滤条件。支持以下条件：\n<li>snapshot-id - Array of String - 是否必填：是 - 按快照ID过滤，每个请求最多可指定10个快照ID。"
      }
    ],
    "desc": "本接口（DescribeSnapshotOperationLogs）用于查询快照操作日志列表。\n\n可根据快照ID过滤。快照ID形如：snap-a1kmcp13。\n"
  },
  "DescribeDiskOperationLogs": {
    "params": [
      {
        "name": "Filters",
        "desc": "过滤条件。支持以下条件：\n<li>disk-id - Array of String - 是否必填：是 - 按云盘ID过滤，每个请求最多可指定10个云盘ID。"
      }
    ],
    "desc": "本接口（DescribeDiskOperationLogs）用于查询云盘操作日志列表。\n\n可根据云盘ID过滤。云盘ID形如：disk-a1kmcp13。\n"
  },
  "CreateSnapshot": {
    "params": [
      {
        "name": "DiskId",
        "desc": "需要创建快照的云硬盘ID，可通过[DescribeDisks](/document/product/362/16315)接口查询。"
      },
      {
        "name": "SnapshotName",
        "desc": "快照名称，不传则新快照名称默认为“未命名”。"
      }
    ],
    "desc": "本接口（CreateSnapshot）用于对指定云盘创建快照。\n\n* 只有具有快照能力的云硬盘才能创建快照。云硬盘是否具有快照能力可由[DescribeDisks](/document/product/362/16315)接口查询，见SnapshotAbility字段。\n* 可创建快照数量限制见[产品使用限制](https://cloud.tencent.com/doc/product/362/5145)。"
  },
  "ModifySnapshotAttribute": {
    "params": [
      {
        "name": "SnapshotId",
        "desc": "快照ID, 可通过[DescribeSnapshots](/document/product/362/15647)查询。"
      },
      {
        "name": "SnapshotName",
        "desc": "新的快照名称。最长为60个字符。"
      },
      {
        "name": "IsPermanent",
        "desc": "快照的保留时间，FALSE表示非永久保留，TRUE表示永久保留。仅支持将非永久快照修改为永久快照。"
      }
    ],
    "desc": "本接口（ModifySnapshotAttribute）用于修改指定快照的属性。\n\n* 当前仅支持修改快照名称及将非永久快照修改为永久快照。\n* “快照名称”仅为方便用户自己管理之用，腾讯云并不以此名称作为提交工单或是进行快照管理操作的依据。"
  },
  "TerminateDisks": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "需退还的云盘ID列表。"
      }
    ],
    "desc": "本接口（TerminateDisks）用于退还云硬盘。\n\n* 不再使用的云盘，可通过本接口主动退还。\n* 本接口支持退还预付费云盘和按小时后付费云盘。按小时后付费云盘可直接退还，预付费云盘需符合退还规则。\n* 支持批量操作，每次请求批量云硬盘的上限为50。如果批量云盘存在不允许操作的，请求会以特定错误码返回。"
  },
  "DescribeDisks": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "按照一个或者多个云硬盘ID查询。云硬盘ID形如：`disk-11112222`，此参数的具体格式可参考API[简介](/document/product/362/15633)的ids.N一节）。参数不支持同时指定`DiskIds`和`Filters`。"
      },
      {
        "name": "Filters",
        "desc": "过滤条件。参数不支持同时指定`DiskIds`和`Filters`。<br><li>disk-usage - Array of String - 是否必填：否 -（过滤条件）按云盘类型过滤。 (SYSTEM_DISK：表示系统盘 | DATA_DISK：表示数据盘)<br><li>disk-charge-type - Array of String - 是否必填：否 -（过滤条件）按照云硬盘计费模式过滤。 (PREPAID：表示预付费，即包年包月 | POSTPAID_BY_HOUR：表示后付费，即按量计费。)<br><li>portable - Array of String - 是否必填：否 -（过滤条件）按是否为弹性云盘过滤。 (TRUE：表示弹性云盘 | FALSE：表示非弹性云盘。)<br><li>project-id - Array of Integer - 是否必填：否 -（过滤条件）按云硬盘所属项目ID过滤。<br><li>disk-id - Array of String - 是否必填：否 -（过滤条件）按照云硬盘ID过滤。云盘ID形如：`disk-11112222`。<br><li>disk-name - Array of String - 是否必填：否 -（过滤条件）按照云盘名称过滤。<br><li>disk-type - Array of String - 是否必填：否 -（过滤条件）按照云盘介质类型过滤。(CLOUD_BASIC：表示普通云硬盘 | CLOUD_PREMIUM：表示高性能云硬盘。| CLOUD_SSD：SSD表示SSD云硬盘。)<br><li>disk-state - Array of String - 是否必填：否 -（过滤条件）按照云盘状态过滤。(UNATTACHED：未挂载 | ATTACHING：挂载中 | ATTACHED：已挂载 | DETACHING：解挂中 | EXPANDING：扩容中 | ROLLBACKING：回滚中 | TORECYCLE：待回收。)<br><li>instance-id - Array of String - 是否必填：否 -（过滤条件）按照云盘挂载的云主机实例ID过滤。可根据此参数查询挂载在指定云主机下的云硬盘。<br><li>zone - Array of String - 是否必填：否 -（过滤条件）按照[可用区](/document/api/213/9452#zone)过滤。<br><li>instance-ip-address - Array of String - 是否必填：否 -（过滤条件）按云盘所挂载云主机的内网或外网IP过滤。<br><li>instance-name - Array of String - 是否必填：否 -（过滤条件）按云盘所挂载的实例名称过滤。<br><li>tag-key - Array of String - 是否必填：否 -（过滤条件）按照标签键进行过滤。<br><li>tag-value - Array of String - 是否必填：否 -（过滤条件）照标签值进行过滤。<br><li>tag:tag-key - Array of String - 是否必填：否 -（过滤条件）按照标签键值对进行过滤。 tag-key使用具体的标签键进行替换。"
      },
      {
        "name": "Offset",
        "desc": "偏移量，默认为0。关于`Offset`的更进一步介绍请参考API[简介](/document/product/362/15633)中的相关小节。"
      },
      {
        "name": "Limit",
        "desc": "返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API [简介](/document/product/362/15633)中的相关小节。"
      },
      {
        "name": "Order",
        "desc": "输出云盘列表的排列顺序。取值范围：<br><li>ASC：升序排列<br><li>DESC：降序排列。"
      },
      {
        "name": "OrderField",
        "desc": "云盘列表排序的依据字段。取值范围：<br><li>CREATE_TIME：依据云盘的创建时间排序<br><li>DEADLINE：依据云盘的到期时间排序<br>默认按云盘创建时间排序。"
      },
      {
        "name": "ReturnBindAutoSnapshotPolicy",
        "desc": "云盘详情中是否需要返回云盘绑定的定期快照策略ID，TRUE表示需要返回，FALSE表示不返回。"
      }
    ],
    "desc": "本接口（DescribeDisks）用于查询云硬盘列表。\n\n* 可以根据云硬盘ID、云硬盘类型或者云硬盘状态等信息来查询云硬盘的详细信息，不同条件之间为与(AND)的关系，过滤信息详细请见过滤器`Filter`。\n* 如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的云硬盘列表。"
  },
  "ModifyDisksRenewFlag": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "一个或多个待操作的云硬盘ID。"
      },
      {
        "name": "RenewFlag",
        "desc": "云盘的续费标识。取值范围：<br><li>NOTIFY_AND_AUTO_RENEW：通知过期且自动续费<br><li>NOTIFY_AND_MANUAL_RENEW：通知过期不自动续费<br><li>DISABLE_NOTIFY_AND_MANUAL_RENEW：不通知过期不自动续费。"
      }
    ],
    "desc": "本接口（ModifyDisksRenewFlag）用于修改云硬盘续费标识，支持批量修改。"
  },
  "DescribeSnapshots": {
    "params": [
      {
        "name": "SnapshotIds",
        "desc": "要查询快照的ID列表。参数不支持同时指定`SnapshotIds`和`Filters`。"
      },
      {
        "name": "Filters",
        "desc": "过滤条件。参数不支持同时指定`SnapshotIds`和`Filters`。<br><li>snapshot-id - Array of String - 是否必填：否 -（过滤条件）按照快照的ID过滤。快照ID形如：`snap-11112222`。<br><li>snapshot-name - Array of String - 是否必填：否 -（过滤条件）按照快照名称过滤。<br><li>snapshot-state - Array of String - 是否必填：否 -（过滤条件）按照快照状态过滤。 (NORMAL：正常 | CREATING：创建中 | ROLLBACKING：回滚中。)<br><li>disk-usage - Array of String - 是否必填：否 -（过滤条件）按创建快照的云盘类型过滤。 (SYSTEM_DISK：代表系统盘 | DATA_DISK：代表数据盘。)<br><li>project-id  - Array of String - 是否必填：否 -（过滤条件）按云硬盘所属项目ID过滤。<br><li>disk-id  - Array of String - 是否必填：否 -（过滤条件）按照创建快照的云硬盘ID过滤。<br><li>zone - Array of String - 是否必填：否 -（过滤条件）按照[可用区](/document/api/213/9452#zone)过滤。<br><li>encrypt - Array of String - 是否必填：否 -（过滤条件）按是否加密盘快照过滤。 (TRUE：表示加密盘快照 | FALSE：表示非加密盘快照。)"
      },
      {
        "name": "Offset",
        "desc": "偏移量，默认为0。关于`Offset`的更进一步介绍请参考API[简介](/document/product/362/15633)中的相关小节。"
      },
      {
        "name": "Limit",
        "desc": "返回数量，默认为20，最大值为100。关于`Limit`的更进一步介绍请参考 API [简介](/document/product/362/15633)中的相关小节。"
      },
      {
        "name": "Order",
        "desc": "输出云盘列表的排列顺序。取值范围：<br><li>ASC：升序排列<br><li>DESC：降序排列。"
      },
      {
        "name": "OrderField",
        "desc": "快照列表排序的依据字段。取值范围：<br><li>CREATE_TIME：依据快照的创建时间排序<br>默认按创建时间排序。"
      }
    ],
    "desc": "本接口（DescribeSnapshots）用于查询快照的详细信息。\n\n* 根据快照ID、创建快照的云硬盘ID、创建快照的云硬盘类型等对结果进行过滤，不同条件之间为与(AND)的关系，过滤信息详细请见过滤器`Filter`。\n*  如果参数为空，返回当前用户一定数量（`Limit`所指定的数量，默认为20）的快照列表。"
  },
  "AttachDisks": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "将要被挂载的弹性云盘ID。通过[DescribeDisks](/document/product/362/16315)接口查询。单次最多可挂载10块弹性云盘。"
      },
      {
        "name": "InstanceId",
        "desc": "云服务器实例ID。云盘将被挂载到此云服务器上，通过[DescribeInstances](/document/product/213/15728)接口查询。"
      },
      {
        "name": "DeleteWithInstance",
        "desc": "可选参数，不传该参数则仅执行挂载操作。传入`True`时，会在挂载成功后将云硬盘设置为随云主机销毁模式，仅对按量计费云硬盘有效。"
      }
    ],
    "desc": "本接口（AttachDisks）用于挂载云硬盘。\n \n* 支持批量操作，将多块云盘挂载到同一云主机。如果多个云盘存在不允许挂载的云盘，则操作不执行，以返回特定的错误码返回。\n* 本接口为异步接口，当挂载云盘的请求成功返回时，表示后台已发起挂载云盘的操作，可通过接口[DescribeDisks](/document/product/362/16315)来查询对应云盘的状态，如果云盘的状态由“ATTACHING”变为“ATTACHED”，则为挂载成功。"
  },
  "ResizeDisk": {
    "params": [
      {
        "name": "DiskId",
        "desc": "云硬盘ID， 通过[DescribeDisks](/document/product/362/16315)接口查询。"
      },
      {
        "name": "DiskSize",
        "desc": "云硬盘扩容后的大小，单位为GB，必须大于当前云硬盘大小。云盘大小取值范围参见云硬盘[产品分类](/document/product/362/2353)的说明。"
      }
    ],
    "desc": "本接口（ResizeDisk）用于扩容云硬盘。\n\n* 只支持扩容弹性云盘。云硬盘类型可以通过[DescribeDisks](/document/product/362/16315)接口查询，见输出参数中Portable字段解释。随云主机创建的云硬盘需通过[ResizeInstanceDisks](/document/product/213/15731)接口扩容。\n* 本接口为异步接口，接口成功返回时，云盘并未立即扩容到指定大小，可通过接口[DescribeDisks](/document/product/362/16315)来查询对应云盘的状态，如果云盘的状态为“EXPANDING”，表示正在扩容中，当状态变为“UNATTACHED”，表示扩容完成。 "
  },
  "DetachDisks": {
    "params": [
      {
        "name": "DiskIds",
        "desc": "将要解挂的云硬盘ID， 通过[DescribeDisks](/document/product/362/16315)接口查询，单次请求最多可解挂10块弹性云盘。"
      }
    ],
    "desc": "本接口（DetachDisks）用于解挂云硬盘。\n\n* 支持批量操作，解挂挂载在同一主机上的多块云盘。如果多块云盘存在不允许解挂载的云盘，则操作不执行，以返回特定的错误码返回。\n* 本接口为异步接口，当请求成功返回时，云盘并未立即从主机解挂载，可通过接口[DescribeDisks](/document/product/362/16315)来查询对应云盘的状态，如果云盘的状态由“ATTACHED”变为“UNATTACHED”，则为解挂载成功。"
  },
  "DescribeDiskConfigQuota": {
    "params": [
      {
        "name": "InquiryType",
        "desc": "查询类别，取值范围。<br><li>INQUIRY_CBS_CONFIG：查询云盘配置列表<br><li>INQUIRY_CVM_CONFIG：查询云盘与实例搭配的配置列表。"
      },
      {
        "name": "Zones",
        "desc": "查询一个或多个[可用区](/document/api/213/9452#zone)下的配置。"
      },
      {
        "name": "DiskChargeType",
        "desc": "付费模式。取值范围：<br><li>PREPAID：预付费<br><li>POSTPAID_BY_HOUR：后付费。"
      },
      {
        "name": "DiskTypes",
        "desc": "硬盘介质类型。取值范围：<br><li>CLOUD_BASIC：表示普通云硬盘<br><li>CLOUD_PREMIUM：表示高性能云硬盘<br><li>CLOUD_SSD：表示SSD云硬盘。"
      },
      {
        "name": "DiskUsage",
        "desc": "系统盘或数据盘。取值范围：<br><li>SYSTEM_DISK：表示系统盘<br><li>DATA_DISK：表示数据盘。"
      },
      {
        "name": "InstanceFamilies",
        "desc": "按照实例机型系列过滤。实例机型系列形如：S1、I1、M1等。详见[实例类型](https://cloud.tencent.com/document/product/213/11518)"
      },
      {
        "name": "CPU",
        "desc": "实例CPU核数。"
      },
      {
        "name": "Memory",
        "desc": "实例内存大小。"
      }
    ],
    "desc": "本接口（DescribeDiskConfigQuota）用于查询云硬盘配额。"
  }
}