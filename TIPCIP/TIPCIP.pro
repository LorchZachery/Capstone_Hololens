#-------------------------------------------------
#
# Project created by QtCreator 2018-02-17T23:47:20
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = TIPCIP
TEMPLATE = app


SOURCES += main.cpp\
        dialog.cpp \
    about.cpp

INCLUDEPATH += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\include"

LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_calib3d242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_contrib242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_core242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_features2d242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_flann242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_gpu242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_highgui242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_imgproc242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_legacy242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_ml242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_nonfree242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_objdetect242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_photo242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_stitching242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_video242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\libopencv_videostab242.dll"
LIBS += "C:\Users\Gonzalo\Desktop\CIP2018\0_opencv\lib\opencv_ffmpeg242.dll"


HEADERS  += dialog.h \
    about.h

FORMS    += dialog.ui \
    about.ui

RC_FILE = myapp.rc

RESOURCES += \
    resources.qrc
