# epj@asc.upenn.edu
# 04/29/2021 

# import modules
library(httpuv)

# set configs
PORTEnv <- Sys.getenv("FUNCTIONS_CUSTOMHANDLER_PORT")
PORT <- strtoi(PORTEnv , base = 0L)

############################
# Set your Status Codes for Errors

http_not_found <- list(
  status=404,
  body='404 Not Found'
)

http_method_not_allowed <- list(
  status=405,
  body='405 Method Not Allowed'
)

############################
# Set your hello world function
# DEVELOPMENT FOR BCRA WOULD LIKELY GO HERE?
# TAKES LIKE 9 QUERY STRINGS... 

hello_handler <- list(
  GET = function (request) {
    list(body=paste(
      "Hello,",
      if(substr(request$QUERY_STRING,1,6)=="?name=") 
        substr(request$QUERY_STRING,7,40) else "World-ATN",
      sep=" "))
  }
)

BCRA_handler <- list(
  GET = function (request) {
    list(body=paste(
      "BCRA R Package API endpoint testing... (epj@asc.upenn.edu)\n",
      if(substr(request$QUERY_STRING)=="?name=") 
        name_bcra = substr(request$QUERY_STRING),
      if(substr(request$QUERY_STRING)=="?AgeM=") 
        agem_bcra = substr(request$QUERY_STRING),
      if(substr(request$QUERY_STRING)=="?Race=") 
        race_bcra = substr(request$QUERY_STRING),
      if(substr(request$QUERY_STRING)=="?xyz=") 
        xyz_bcra = substr(request$QUERY_STRING),
      sep=" ")
      
      ##############################
      # TODO --> 
      # How to take QUERY_STRING 9 values from URL and 
      # then basically create our dataframe to run against BCRA
      # for the absolute risk calculator...
      
      )
  }
) 

############################
# Set your routes for the api

routes <- list(
  '/api/HttpExample' = hello_handler
  '/api/BCRAExample' = BCRA_handler # <-- not working of course...
)

############################
# Create router function which prepares request

router <- function (routes, request) {
  
  if (!request$PATH_INFO %in% names(routes)) {
    return(http_not_found) # <-- 404 status, if request is NOT in routes list
  }
  path_handler <- routes[[request$PATH_INFO]] # <-- set path handler

  if (!request$REQUEST_METHOD %in% names(path_handler)) {
    return(http_method_not_allowed) # <-- 405 status, if request is NOT in path handler
  }
  method_handler <- path_handler[[request$REQUEST_METHOD]] # <-- set method handler

  return(method_handler(request)) # <-- return method handler
}

############################
# Create app call function to prepare response

app <- list(
  call = function (request) {

    response <- router(routes, request) # <-- create response for router function

    if (!'status' %in% names(response)) {
      response$status <- 200 # <-- 200 if status is NOT in response 
      # Please note -- 404 and 405 response has an explicit status,
      # the hello_handler does not set a status, so we do it here!
    }

    if (!'headers' %in% names(response)) {
      response$headers <- list() # <-- create empty list of headers if NOT in response
    }

    if (!'Content-Type' %in% names(response$headers)) {
      response$headers[['Content-Type']] <- 'text/plain' # <-- set header to just simple plain text
    }

    return(response) # <-- return response with status, header, and body
  }
)

# finally, run our httpuv server!
cat(paste0("Server listening on :", PORT, "...\n"))
runServer("0.0.0.0", PORT, app)