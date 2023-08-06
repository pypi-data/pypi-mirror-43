"""Infer a nested object from a schema."""
import jsonschema

from opentea.noob.noob import nob_pprint

def nob_complete(schema, update_data=None):
    """Infer a nested object from a schema.

    Input :
    -------
    schema :  a schema object
    update_data : nested object, providing known
        parts of the object to infer

    Output :
    --------
    nob_out : nested object
    """

    out = recursive_infer(schema,
                          path=None,
                          update_data=update_data)
    #print(nob_pprint(out))
    jsonschema.validate(out, schema)
    return out


def recursive_infer(schema, path, update_data=None):
    """Recursive inference.

    Input :
    -------
    schema :  a schema object
    update_data : nested object, providing known
        parts of the object to infer

    Output :
    --------
    nob_out : nested object
    """
    if path is None:
        path = list()
    out = None
    if isinstance(schema, dict):
        if "type" in schema:
            if schema["type"] == "object":
                if "properties" in schema:
                    out = recursive_infer_properties(
                        schema["properties"],
                        path,
                        update_data)
                else:
                    print("____")
                    print(nob_pprint(schema, max_lvl=2))
                    print("----")
                    raise RuntimeError(
                        "Cannot infer objects without properties")
            elif schema["type"] in ["string",
                                    "integer",
                                    "number",
                                    "boolean"]:
                out = recursive_infer_leafs(schema, path, update_data)
            elif schema["type"] == "array":
                out = recursive_infer_array(schema, path, update_data)

        elif "oneOf" in schema:
            out = recursive_infer_oneof(schema, path, update_data)
        else:
            out = recursive_infer_properties(schema, path, update_data)
    else:
        
        print("____")
        print("At path : " + "/".join(path))
        
        print(nob_pprint(schema, max_lvl=2))
        print("----")
        raise RuntimeError("Dead end.")

    if out is None:
        print("____")
        print("At path : " + "/".join(path))
        print(nob_pprint(schema, max_lvl=2))
        print("----")
        raise NotImplementedError("Could not infer schema")

    return out


def recursive_infer_leafs(schema, path, update_data=None, ):
    """Recursive inference specific to leafs."""
    out = None
    if "enum" in schema:
        out = schema["enum"][0]
    if "default" in schema:
        out = schema["default"]

    if out is None:
        if schema["type"] == "string":
            out = ""
        elif schema["type"] in ["integer", "number"]:
            out = infer_number(schema)
        elif schema["type"] == "boolean":
            out = False
        else:
            out = None
    if update_data is not None:
        out = update_data
    return out

def infer_number(schema):
    """Return default number if not provided by schema"""
    out = 0.0
    if schema["type"] == "integer":
        out = 0


    if "maximum" in schema:
        out = schema["maximum"]
        if "exclusiveMaximum" in schema:
            if schema["exclusiveMaximum"]:
                if isinstance(out, float):
                    out *= 0.9
                elif isinstance(out, int):
                    out -= 1
    if "minimum" in schema:
        out = schema["minimum"]
        if "exclusiveMinimum" in schema:
            if schema["exclusiveMinimum"]:
                if isinstance(out, float):
                    out *= 1.1
                elif isinstance(out, int):
                    out += 1
    return out


def recursive_infer_oneof(schema, path, update_data=None):
    """Recursive inference specific to oneOfs."""
    key = schema["oneOf"][0]["required"][0]
    option_schema = schema["oneOf"][0]["properties"]
    option_data = None

    if isinstance(update_data, dict):
        if update_data != {}:
            for update_key in update_data.keys():
                key = update_key
                break
            for option in schema["oneOf"]:
                if option["required"][0] == key:
                    option_data = update_data[key]
                    option_schema = option["properties"]

    out = dict()
    out[key] = recursive_infer(option_schema[key], [*path, key], option_data)
    return out


def recursive_infer_array(schema, path, update_data=None, ):
    """Recursive inference specific to arrays."""
    out = list()
    default_len = 3
    if "maxItems" in schema:
        default_len = min(default_len, schema["maxItems"])
    if "minItems" in schema:
        default_len = max(default_len, schema["minItems"])

    if "items" in schema:
        if isinstance(update_data, list):
            for i, item_data in enumerate(update_data):
                out.append(recursive_infer(schema["items"], [*path, i], item_data))
        else:
            for i in range(default_len):
                out.append(recursive_infer(schema["items"], [*path, i]))
    else:
        for index in range(default_len):
            out.append("item_#"+str(index))

    if "default" in schema:
        out = schema["default"]
        
    return out


def recursive_infer_properties(schema, path, update_data=None):
    """Recursive inference specific to properties."""
    out = dict()
    for key in schema:
        option_data = None
        if isinstance(update_data, dict):
            if key in update_data:
                option_data = update_data[key]
        out[key] = recursive_infer(schema[key], [*path, key],  option_data)
    return out
