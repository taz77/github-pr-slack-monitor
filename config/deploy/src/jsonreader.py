import json


class JsonReader(object):
    def json_to_read(self, argument):
        """
        Dispatch method to read JSON
        """

        switcher = {
            "dev": "jsondev",
            "test": "jsontest",
            "preprod": "jsonpreprod",
            "prod": "jsonprod"
        }

        method_name = switcher.get(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid environment")
        # Call the method as we return it
        return method()

    def jsondev(self):
        with open('dev.json') as f:
            data = json.load(f)
        return data

    def jsontest(self):
        with open('test.json') as f:
            data = json.load(f)
        return data

    def jsonpreprod(self):
        with open('preprod.json') as f:
            data = json.load(f)
        return data

    def jsonprod(self):
        with open('prod.json') as f:
            data = json.load(f)
        return data
