# Newspan

With the demise of Google Reader, everyone is making RSS readers that suck a little. We are not the exception.

 * self-hosted RSS reader
 * labels, stars as expected
 * unlike some feed readers, we honour `xml:base`
 * keyboard shortcuts
 * Heroku compatible

## Environment variables for Heroku

 * DJANGO_SECRET_KEY=something secret
 * DJANGO_DEBUG=false
 * ALLOWED_HOSTS=your Heroku app hostname
 * AWS_ACCESS_KEY_ID
 * AWS_SECRET_ACCESS_KEY
 * AWS_STORAGE_BUCKET_NAME
 * FULLY_SECURE=true # plus enable SSL and certs:add

## The team

 * Gabor Javorszky
 * Mark Norman Francis
 * James Aylett
 * Ryan Alexander
