# TODO:
# 
# create Milestones
# 
# add logic to handle VT (time-fuze and proxy rounds)
    # add args arming_distance and trigger_radius
    # parse html table # it will get messier :yaay:
# 
# find/parse/calulate armament diameter
# 
# determine if a gun is a "main armament"
# 
# move armament parsing to separate file
# 
# move ammunition parsing to separate file
# 
# add G6 to tank list
# 
# handle changelog 
    # compare with last check
    # grab changelog
    # parse it
    # check for changes
        # check if vehicle is available
        # parse changes
        # update
    # save to DB
# 
# add DB
    # create DB models
    # add tables
        # metadata
            # last changelog update time 
            # nations 
            # ranks
            # 
        # ground vehicle
        # ground armaments
        # ground ammunition
        # aerial vehicles
        # aerial ammunition 
        # naval vehicle 
        # naval ammunition
# 
# create docker-compose setup
    # with virtual drive integration thing 
    # DB in dedicated Container
    # management container # or making sure the server doesn't crash unnoticed
# 
# check if specific routes can be called locally ONLY -> used for updating (I guess)
# 
# create a user counter
# 
# check for module that can compare files (just like meld) and "target" specific blocks 
    # don't update/parse when unnessessary data changes  
# 
# argparsing for scrape, enforce fresh scrape
# 
# 
# 