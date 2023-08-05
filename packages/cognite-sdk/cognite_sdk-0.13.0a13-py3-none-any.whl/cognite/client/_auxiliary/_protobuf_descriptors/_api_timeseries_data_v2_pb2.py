# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api_timeseries_data_v2.proto

import sys

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pb2
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="api_timeseries_data_v2.proto",
    package="api.v2",
    syntax="proto3",
    serialized_pb=_b(
        '\n\x1c\x61pi_timeseries_data_v2.proto\x12\x06\x61pi.v2"3\n\x0fStringDatapoint\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\t"4\n\x10NumericDatapoint\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x01"?\n\x14StringTimeseriesData\x12\'\n\x06points\x18\x01 \x03(\x0b\x32\x17.api.v2.StringDatapoint"A\n\x15NumericTimeseriesData\x12(\n\x06points\x18\x01 \x03(\x0b\x32\x18.api.v2.NumericDatapoint"\x82\x01\n\x0eTimeseriesData\x12\x32\n\nstringData\x18\x01 \x01(\x0b\x32\x1c.api.v2.StringTimeseriesDataH\x00\x12\x34\n\x0bnumericData\x18\x02 \x01(\x0b\x32\x1d.api.v2.NumericTimeseriesDataH\x00\x42\x06\n\x04\x64\x61ta"\x95\x01\n\x13NamedTimeseriesData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x32\n\nstringData\x18\x02 \x01(\x0b\x32\x1c.api.v2.StringTimeseriesDataH\x00\x12\x34\n\x0bnumericData\x18\x03 \x01(\x0b\x32\x1d.api.v2.NumericTimeseriesDataH\x00\x42\x06\n\x04\x64\x61ta"T\n\x18MultiNamedTimeseriesData\x12\x38\n\x13namedTimeseriesData\x18\x01 \x03(\x0b\x32\x1b.api.v2.NamedTimeseriesDataB1\n\x17\x63om.cognite.data.api.v2P\x01\xaa\x02\x13\x43ognite.Data.Api.V2b\x06proto3'
    ),
)


_STRINGDATAPOINT = _descriptor.Descriptor(
    name="StringDatapoint",
    full_name="api.v2.StringDatapoint",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="timestamp",
            full_name="api.v2.StringDatapoint.timestamp",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="api.v2.StringDatapoint.value",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=40,
    serialized_end=91,
)


_NUMERICDATAPOINT = _descriptor.Descriptor(
    name="NumericDatapoint",
    full_name="api.v2.NumericDatapoint",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="timestamp",
            full_name="api.v2.NumericDatapoint.timestamp",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="api.v2.NumericDatapoint.value",
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=93,
    serialized_end=145,
)


_STRINGTIMESERIESDATA = _descriptor.Descriptor(
    name="StringTimeseriesData",
    full_name="api.v2.StringTimeseriesData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="points",
            full_name="api.v2.StringTimeseriesData.points",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=147,
    serialized_end=210,
)


_NUMERICTIMESERIESDATA = _descriptor.Descriptor(
    name="NumericTimeseriesData",
    full_name="api.v2.NumericTimeseriesData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="points",
            full_name="api.v2.NumericTimeseriesData.points",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=212,
    serialized_end=277,
)


_TIMESERIESDATA = _descriptor.Descriptor(
    name="TimeseriesData",
    full_name="api.v2.TimeseriesData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="stringData",
            full_name="api.v2.TimeseriesData.stringData",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="numericData",
            full_name="api.v2.TimeseriesData.numericData",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="data", full_name="api.v2.TimeseriesData.data", index=0, containing_type=None, fields=[]
        )
    ],
    serialized_start=280,
    serialized_end=410,
)


_NAMEDTIMESERIESDATA = _descriptor.Descriptor(
    name="NamedTimeseriesData",
    full_name="api.v2.NamedTimeseriesData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="api.v2.NamedTimeseriesData.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="stringData",
            full_name="api.v2.NamedTimeseriesData.stringData",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="numericData",
            full_name="api.v2.NamedTimeseriesData.numericData",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="data", full_name="api.v2.NamedTimeseriesData.data", index=0, containing_type=None, fields=[]
        )
    ],
    serialized_start=413,
    serialized_end=562,
)


_MULTINAMEDTIMESERIESDATA = _descriptor.Descriptor(
    name="MultiNamedTimeseriesData",
    full_name="api.v2.MultiNamedTimeseriesData",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="namedTimeseriesData",
            full_name="api.v2.MultiNamedTimeseriesData.namedTimeseriesData",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=564,
    serialized_end=648,
)

_STRINGTIMESERIESDATA.fields_by_name["points"].message_type = _STRINGDATAPOINT
_NUMERICTIMESERIESDATA.fields_by_name["points"].message_type = _NUMERICDATAPOINT
_TIMESERIESDATA.fields_by_name["stringData"].message_type = _STRINGTIMESERIESDATA
_TIMESERIESDATA.fields_by_name["numericData"].message_type = _NUMERICTIMESERIESDATA
_TIMESERIESDATA.oneofs_by_name["data"].fields.append(_TIMESERIESDATA.fields_by_name["stringData"])
_TIMESERIESDATA.fields_by_name["stringData"].containing_oneof = _TIMESERIESDATA.oneofs_by_name["data"]
_TIMESERIESDATA.oneofs_by_name["data"].fields.append(_TIMESERIESDATA.fields_by_name["numericData"])
_TIMESERIESDATA.fields_by_name["numericData"].containing_oneof = _TIMESERIESDATA.oneofs_by_name["data"]
_NAMEDTIMESERIESDATA.fields_by_name["stringData"].message_type = _STRINGTIMESERIESDATA
_NAMEDTIMESERIESDATA.fields_by_name["numericData"].message_type = _NUMERICTIMESERIESDATA
_NAMEDTIMESERIESDATA.oneofs_by_name["data"].fields.append(_NAMEDTIMESERIESDATA.fields_by_name["stringData"])
_NAMEDTIMESERIESDATA.fields_by_name["stringData"].containing_oneof = _NAMEDTIMESERIESDATA.oneofs_by_name["data"]
_NAMEDTIMESERIESDATA.oneofs_by_name["data"].fields.append(_NAMEDTIMESERIESDATA.fields_by_name["numericData"])
_NAMEDTIMESERIESDATA.fields_by_name["numericData"].containing_oneof = _NAMEDTIMESERIESDATA.oneofs_by_name["data"]
_MULTINAMEDTIMESERIESDATA.fields_by_name["namedTimeseriesData"].message_type = _NAMEDTIMESERIESDATA
DESCRIPTOR.message_types_by_name["StringDatapoint"] = _STRINGDATAPOINT
DESCRIPTOR.message_types_by_name["NumericDatapoint"] = _NUMERICDATAPOINT
DESCRIPTOR.message_types_by_name["StringTimeseriesData"] = _STRINGTIMESERIESDATA
DESCRIPTOR.message_types_by_name["NumericTimeseriesData"] = _NUMERICTIMESERIESDATA
DESCRIPTOR.message_types_by_name["TimeseriesData"] = _TIMESERIESDATA
DESCRIPTOR.message_types_by_name["NamedTimeseriesData"] = _NAMEDTIMESERIESDATA
DESCRIPTOR.message_types_by_name["MultiNamedTimeseriesData"] = _MULTINAMEDTIMESERIESDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StringDatapoint = _reflection.GeneratedProtocolMessageType(
    "StringDatapoint",
    (_message.Message,),
    dict(
        DESCRIPTOR=_STRINGDATAPOINT,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.StringDatapoint)
    ),
)
_sym_db.RegisterMessage(StringDatapoint)

NumericDatapoint = _reflection.GeneratedProtocolMessageType(
    "NumericDatapoint",
    (_message.Message,),
    dict(
        DESCRIPTOR=_NUMERICDATAPOINT,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.NumericDatapoint)
    ),
)
_sym_db.RegisterMessage(NumericDatapoint)

StringTimeseriesData = _reflection.GeneratedProtocolMessageType(
    "StringTimeseriesData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_STRINGTIMESERIESDATA,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.StringTimeseriesData)
    ),
)
_sym_db.RegisterMessage(StringTimeseriesData)

NumericTimeseriesData = _reflection.GeneratedProtocolMessageType(
    "NumericTimeseriesData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_NUMERICTIMESERIESDATA,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.NumericTimeseriesData)
    ),
)
_sym_db.RegisterMessage(NumericTimeseriesData)

TimeseriesData = _reflection.GeneratedProtocolMessageType(
    "TimeseriesData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_TIMESERIESDATA,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.TimeseriesData)
    ),
)
_sym_db.RegisterMessage(TimeseriesData)

NamedTimeseriesData = _reflection.GeneratedProtocolMessageType(
    "NamedTimeseriesData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_NAMEDTIMESERIESDATA,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.NamedTimeseriesData)
    ),
)
_sym_db.RegisterMessage(NamedTimeseriesData)

MultiNamedTimeseriesData = _reflection.GeneratedProtocolMessageType(
    "MultiNamedTimeseriesData",
    (_message.Message,),
    dict(
        DESCRIPTOR=_MULTINAMEDTIMESERIESDATA,
        __module__="api_timeseries_data_v2_pb2"
        # @@protoc_insertion_point(class_scope:api.v2.MultiNamedTimeseriesData)
    ),
)
_sym_db.RegisterMessage(MultiNamedTimeseriesData)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(
    descriptor_pb2.FileOptions(), _b("\n\027com.cognite.data.api.v2P\001\252\002\023Cognite.Data.Api.V2")
)
# @@protoc_insertion_point(module_scope)
