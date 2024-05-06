class Commons:

    @staticmethod
    def config(k):
        with open(f'/configs/default/parameters/{k}', 'r') as f:
            return f.read()

    @staticmethod
    def auth():
        return (Commons.config("ES_USERNAME"), Commons.config("ES_PASSWORD"))

    @staticmethod
    def search_url():
        return f'{Commons.config("ES_URL")}/{Commons.config("ES_DATABASE")}/_search'


