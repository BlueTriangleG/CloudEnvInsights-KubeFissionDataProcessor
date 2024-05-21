1. http://$FISSION_ROUTER/database/{datatype:[a-zA-Z0-9-]+}
Use this restful api to access this function in fission where datatype is the data topic name.

2. http://$FISSION_ROUTER/database/{datatype:[a-zA-Z0-9-]+}/{startdate:[0-9]{4}-[0-1][0-9]-[0-3][0-9]-[0-2][0-9]}/{enddate:[0-9]{4}-[0-1][0-9]-[0-3][0-9]-[0-2][0-9]}
Use this restful api to access this function in fission. where datatype is: the database where your database is located. startdate is the start time of the time range and enddate is the end time of the time range.

3. http://$FISSION_ROUTER/database/{datatype:[a-zA-Z0-9-]+}
Use this restful api for the put-database function in fisison, where dabase is the name of the database topic you want to transfer data to. You need to transfer a json file.