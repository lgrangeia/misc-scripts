@echo off

@echo "Simple APK sign script."
echo "'keytool' and 'jarsigner' are usually in \Android Studio\jre\bin\"
echo "Add it to your PATH."

if "%1"=="" (
	echo "usage: %0 <apk_to_sign.apk>"
	exit
)

if not exist my.keystore (
	rem create java keystore
	keytool -genkey -v -keystore my.keystore -alias mykeyaliasname -keyalg RSA -keysize 2048 -storepass mystorepass -validity 10000
)

rem sign the APK
jarsigner -sigalg SHA1withRSA -digestalg SHA1 -keystore my.keystore -storepass mystorepass %1 mykeyaliasname

rem verify the signature you just created
jarsigner -verify %1
