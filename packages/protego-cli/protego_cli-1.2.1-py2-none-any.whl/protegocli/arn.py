class Arn(object):
    # arn:partition:service:region:account-id:resource
    supported_service = "base"

    def __init__(self, arn_str):
        if arn_str is None or len(arn_str.split(":")) < 6:
            raise ValueError("Unknown ARN format. ARN: " + str(arn_str))
        self.arn_str = arn_str
        self.arn_split = arn_str.split(":")

        if self.supported_service != "base" and self.service != self.supported_service:
            raise ValueError("Class " +self.__class__.__name__+ " support only service : " + self.supported_service + " Invalid service " + self.service)


    def __str__(self):
        return ":".join(self.arn_split)

    @property
    def str(self):
        return self.__str__()

    @property
    def partition(self):
        return self.arn_split[1]

    @property
    def service(self):
        return self.arn_split[2]

    @property
    def region(self):
        return self.arn_split[3]

    @property
    def account(self):
        return self.arn_split[4]

class ArnLambda(Arn):
    # arn:aws:lambda:region:account-id:function:function-name:version
    supported_service = "lambda"

    @property
    def function_name(self):
        return self.arn_split[6]
