
from .base_action import *


@Actions.register("resultset_to_form")
class ResultSetToFormAction(BaseAction):
    """
    Convert a dict into form data
    {a:1, b:2} => data[a]=1&data[b]=2
    {{a:1, b:2}, {a:3, b:4}} => data[0][a]=1&data[0][b]=2&data[1][a]=3&data[1][b]=4
    :param key_value_attributes || list
    """

    def result_set_to_form_data2(self, dict_list, key_value_attributes, context):
        result = dict()
        index = 0
        for d in dict_list:
            for item in key_value_attributes:
                (key, value) = item
                form_key = "data[%d][%s]" % (index, key)
                result[form_key] = context.evaluate(value)

            index += 1
        return result


    def result_set_to_form_data(self, dict_list, key_value_attributes_map):
        """
        :Deprecated
        """
        result = dict()
        index = 0
        for d in dict_list:
            for key, value in d.items():
                data_key = key
                convert = ""
                if key in key_value_attributes_map:
                    attr = key_value_attributes_map[key]
                    data_key = attr[0]
                    if len(attr) > 1:
                        convert = key_value_attributes_map[key][1]
                else:
                    continue
                # ["SomeKey", "", ""], if set the second empty string, 
                # it would prevent transform this field in the destination dict
                if data_key == "":
                    continue
                key = "data[%d][%s]" % (index, data_key)
                if convert == "":
                    result[key] = value
                else:
                    # TODO:
                    from convertor import Converters
                    result[key] = Converters.get(convert)(value)
            index += 1
        return result

    def execute(self, context):
        action_config = self.get_action_config()
        # Mapping of src table fields => dest table fields
        key_value_attributes = action_config['key_value_attributes']
        
        param0 = self.get_param_var_name()

        data = context.get_context_var(param0)
        self.log(data)
        value = self.result_set_to_form_data2(data, key_value_attributes, context)
        print(value)
        return_var = self.get_return_var_name()

        context.set_context_var(return_var, value)