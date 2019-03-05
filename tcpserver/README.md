- dev

device(dev) --> `"%s.%d", macchar, cc` --> deviceid, pin, pin_id 

--> query shopid with device id;

--> update cached stats with pin_id;

--> broadcast shopid pin_id;

- remote

device(remote) --> `"hb.%s.%ld.%s", macchar, value, sigState`

--> query shopid with device id in cache -->

if exist, update device status

if not, query device id in sql -->

if exist, add to cache and update status

if not, push to sql: new device, waiting to be allocated

