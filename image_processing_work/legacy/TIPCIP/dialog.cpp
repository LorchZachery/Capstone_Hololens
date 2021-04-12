#include "dialog.h"
#include "ui_dialog.h"
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/opencv.hpp"
#include <QMessageBox>
#include <QFileDialog>
#include <QProcess>
#include <QTextStream>
#include <QFile>
#include <QDataStream>
#include <string>
#include <QIODevice>
#include <QThread>
#include <QDateTime>
#include <fstream>
#include <sstream>

using namespace cv;

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    ui->setupUi(this);

    // Initialize Font Title
    QFont font = ui->l_title->font();
    font.setPointSize(16);
    font.setBold(true);
    ui->l_title->setFont(font);

    // Initialize Graphics
    scene = new QGraphicsScene(this);

    // Initialize ListView(s)
    ui->lst_imagefile->setModel(new QStringListModel(m_slData));
    ui->lst_outdir->setModel(new QStringListModel(m_slOutdir));
    ui->lst_outfiles->setModel(new QStringListModel(m_slOutfiles));

    // Control variables - Initialization
    flaghito = false;

    // Test openCV
    // Mat img;
    AboutDlg = new about(this);
}

Dialog::~Dialog()
{
    delete ui;


}

void Dialog::on_pb_addimage_clicked()
{
    QMessageBox* msgBox;

    msgBox = new QMessageBox(this);                                                         /* Creation of the MessageBox*/
    msgBox->setIcon(QMessageBox::Question);                                                 /* Setting icon */
    msgBox->setText("Please select if you want to work with files or directories (it should contain only images): ");  /*Text in the messagebox */
    QPushButton *Files_btn = msgBox->addButton(tr("Files"),QMessageBox::ActionRole);        /* Creating buttons for the message box */
    QPushButton *Folder_btn = msgBox->addButton(tr("Directories"),QMessageBox::ActionRole);
    QPushButton *Cancel_btn = msgBox->addButton(QMessageBox::Cancel);

    msgBox->exec();

    if(msgBox->clickedButton()== Files_btn)
    {
        QStringList fileNames = QFileDialog::getOpenFileNames(this,tr("Open files"),"",tr("JPEG(*.jpg *.jpeg);;BMP(*.bmp);;TIFF(*.tif);; All files (*.*)"));

         if(fileNames.size()>0)
         {
             for(int i=0;i<fileNames.size();i++)
             {
                 m_slData.append(fileNames.at(i));
                 ((QStringListModel*) ui->lst_imagefile->model())->setStringList(m_slData);
             }
         }
    }
    else if(msgBox->clickedButton()== Folder_btn)
    {
        QString dir = QFileDialog::getExistingDirectory(this,tr("Open directory"),"",QFileDialog::ShowDirsOnly|QFileDialog::DontResolveSymlinks);

        if (dir != NULL)
        {
            QDir directory(dir);
            QStringList filters;
            filters << "*.jpg" << "*.JPEG";
            QStringList files;
            files = directory.entryList(filters,QDir::Files|QDir::NoSymLinks);
            //printf("%d",files.size());

            if (files.size()>0)
            {
                for(int i=0;i<files.size();i++)
                {
                    QString absPath = directory.absoluteFilePath(files.at(i));
                    m_slData.append(absPath);
                    ((QStringListModel*) ui->lst_imagefile->model())->setStringList(m_slData);
                }
            }

        }
    }
    else if(msgBox->clickedButton()== Cancel_btn)
    {}
}

void Dialog::on_lst_imagefile_clicked(const QModelIndex &index)
{
    if (m_slData.count() == 0)
            return;

    QString filename;
    QPixmap pixmp;
    filename = m_slData.at(index.row());
    pixmp = QPixmap(filename);
    scene->clear();
    scene->addPixmap(pixmp);
    scene->setSceneRect(0,0,pixmp.width(),pixmp.height());
    ui->graphicsView->setScene(scene);
//    QRectF bounds = scene->itemsBoundingRect();
    ui->graphicsView->fitInView(scene->sceneRect(),Qt::IgnoreAspectRatio);
}

void Dialog::on_pb_deleteitem_clicked()
{
    QModelIndexList index = ui->lst_imagefile->selectionModel()->selectedIndexes();
    if(!index.isEmpty())
    {
        ui->lst_imagefile->model()->removeRow(index.at(0).row()); //Remover en el listview
        m_slData.removeAt(index.at(0).row());                     // Remover en la lista de strings
    }
    scene->clear();
}

void Dialog::on_pb_deleteall_clicked()
{
    int cont_data = m_slData.count();

    if(cont_data>0)
    {
        for(int i=0;i<cont_data;i++)
        {
            m_slData.removeLast();
        }
        ((QStringListModel*) ui->lst_imagefile->model())->setStringList(m_slData);
    }

    scene->clear();
}

void Dialog::on_pb_generate_clicked()
{
    printf("JAJAJA");
    // Verifying output directory
    if(m_slOutdir.isEmpty()|| m_slOutdir.count()<1)
    {
        QMessageBox::warning(this,"Warning","The process needs an Output directory to start.\n Press \"Select output directory\" button.",QMessageBox::Ok);
        return;
    }

    // Verifying images in the system
    if(m_slData.isEmpty()|| m_slData.count()<2)
    {
        QMessageBox::warning(this,"Warning","The process needs more than one image to start.\n Press \"Add image(s)\" button.",QMessageBox::Ok);
        return;
    }

    // Verifying pair number of images
    int num_images = m_slData.count();
    if (num_images%2 != 0)
    {
        QMessageBox::warning(this,"Warning","It doesn't exist a even number of images.\nVerify the input images.",QMessageBox::Ok);
        return;
    }

    // Variable Initiation
    int num_iter = m_slData.count()/2;
    int offset = num_iter;
    Mat imgRGB, imgIR;
    double emi=0;
    double refle=0;
    /* File for results */
    FILE *pFile;
    QString ResCSV = m_slOutdir.at(0) + "/result.csv";
    pFile = fopen(ResCSV.toStdString().c_str(),"w");
    if (pFile == NULL)
    {
        QMessageBox::critical(this,"Warning","Result file cannot be created. \n Verify your user's privileges.",QMessageBox::Ok);
        return;
     }
    //fprintf(pFile,"Image number, Emisivity, Reflected Temp, Average Temp, Date\n");
    fprintf(pFile,"Image number, Time, Average Temp\n");

    int id = 0;
    if (flaghito)
        printf("yes\n");
    else
        printf("no\n");

    /* Directories for results */
    QDir directory(m_slOutdir.at(0));
    QString path0("0Aligned");
    QString path1("1PartRGB");
    QString path2("2Mascara");
    QString path3("3tempmask");
    directory.mkdir(path0);
    directory.mkdir(path1);
    directory.mkdir(path2);
    directory.mkdir(path3);


       // MAIN LOOP
 for (id = 0; id<num_iter; id++) {
   // int id = 0;

    // Reading images
    //***** imgRGB = imread(m_slData.at(id).toStdString(),IMREAD_UNCHANGED);
    //***** imgIR = imread(m_slData.at(id+offset).toStdString(),IMREAD_UNCHANGED);
    imgIR = imread(m_slData.at(id*2).toStdString(),IMREAD_UNCHANGED); ///*****
    imgRGB = imread(m_slData.at(id*2+1).toStdString(),IMREAD_UNCHANGED); ////***

    // Getting the CODE (4 digit) to compare with the excel values - The value comes from RGB image
//    int lenstr = m_slData.at(id*2+1).toStdString().size();
//    std::string str = m_slData.at(id*2+1).toStdString().substr(lenstr-8,4);
//    double code = (double) std::atoi(str.c_str());

    int lenstr = m_slData.at(id*2+1).toStdString().size();
    std::string str = m_slData.at(id*2+1).toStdString();
    int index_t;
    bool found = false;
    double code2 = 0;
    int exp = 0;
    for(index_t=lenstr-1; index_t>=0; index_t--)
    {
        if (str.at(index_t)=='.')
        {   found = true;
            printf("Found");
            continue;
        }
        if (found)
        {
           if ((str.at(index_t) >= '0')&&(str.at(index_t) <='9'))
           {
               printf("numnum, index%d, val=%c\n", index_t,str.at(index_t));
               code2 = code2 + ((int)(str.at(index_t)) - 48) *pow(10,exp);
               exp++;
           }
           else
           {
               found = false;
           }
        }
    }
    //printf("CODE: %f\n", code2);
    //std::string str2 = m_slData.at(id*2+1).toStdString().substr(lenstr-8,4);
    //double code = (double) std::atoi(str2.c_str());
    double code = code2;


    // Updating progress bar
    if (num_iter > 1)
        ui->pbar_status->setValue(round(id*100/(num_iter-1)));
    else
        ui->pbar_status->setValue(100);

    // Temperature Correction
    if (flaghito) //There is a file
    {
        int tempCsv = matchCodeCsv(code);
        if (tempCsv>0)
        {
            emi=*(dataCSV+(tempCsv-1)*3+1);
            refle=*(dataCSV+(tempCsv-1)*3+2);
            continue;
        }
        else
        {
            //get_temperature(true,m_slData.at(id+offset),&emi,&refle); // Get temperature from IR image
            get_temperature(true,m_slData.at(id*2),&emi,&refle); // Get temperature from IR image
            //printf("ajaj");
            //printf("\nDATA: %f %f %f\n", *(T_obj), *(T_obj+1), *(T_obj+2));
        }

    }
    else  // There is no file
    {
        //get_temperature(false,m_slData.at(id+offset),&emi,&refle);
        get_temperature(false,m_slData.at(id*2),&emi,&refle);
        printf("\nDATA: %f %f %f\n", *(T_obj), *(T_obj+1), *(T_obj+2));
        printf("\n%f,%f\n",emi,refle);
    }

    // Alignment for pictures saved
    Mat imgIR2;
    Mat Zeros(imgRGB.rows,imgRGB.cols,CV_8UC3,Scalar::all(0));
    Mat Aligned(imgRGB.rows,imgRGB.cols,CV_8UC3,Scalar::all(0));
    Size size_scale(870,640);
    cv::resize(imgIR, imgIR2, size_scale);

    int y_ini = 504;
    int x_ini = 597;

    for (int idy=0; idy<imgIR2.rows; idy++)
    {
        for (int idx=0; idx<imgIR2.cols; idx++)
        {
            Zeros.at<cv::Vec3b>(y_ini+idy,x_ini+idx)[0] = imgIR2.at<cv::Vec3b>(idy,idx)[0];
            Zeros.at<cv::Vec3b>(y_ini+idy,x_ini+idx)[1] = imgIR2.at<cv::Vec3b>(idy,idx)[1];
            Zeros.at<cv::Vec3b>(y_ini+idy,x_ini+idx)[2] = imgIR2.at<cv::Vec3b>(idy,idx)[2];
        }
    }

    for (int idy=0; idy<imgRGB.rows; idy++)
    {
        for (int idx=0; idx<imgRGB.cols; idx++)
        {
            int temp = round(0.5*Zeros.at<cv::Vec3b>(idy,idx)[0] + 0.5*imgRGB.at<cv::Vec3b>(idy,idx)[0]);
            if (temp>255) temp = 255;
            Aligned.at<cv::Vec3b>(idy,idx)[0] = (unsigned char)temp;
            temp = round(0.5*Zeros.at<cv::Vec3b>(idy,idx)[1] + 0.5*imgRGB.at<cv::Vec3b>(idy,idx)[1]);
            if (temp>255) temp = 255;
            Aligned.at<cv::Vec3b>(idy,idx)[1] = (unsigned char)temp;
            temp = round(0.5*Zeros.at<cv::Vec3b>(idy,idx)[2] + 0.5*imgRGB.at<cv::Vec3b>(idy,idx)[2]);
            if (temp>255) temp = 255;
            Aligned.at<cv::Vec3b>(idy,idx)[2] = (unsigned char)temp;
        }
    }

    QString fileAligned = m_slOutdir.at(0) + "/0Aligned/0Aligned_"+ QString::number((int)code) +".jpg";
    imwrite(fileAligned.toStdString().c_str(),Aligned);

    // Aligment for average temperature
    Mat cuttedRGB1=imgIR2.clone();
    for (int idy=0; idy<imgIR2.rows; idy++)
    {
        for (int idx=0; idx<imgIR2.cols; idx++)
        {
            cuttedRGB1.at<cv::Vec3b>(idy,idx)[0] = imgRGB.at<cv::Vec3b>(y_ini+idy,x_ini+idx)[0];
            cuttedRGB1.at<cv::Vec3b>(idy,idx)[1] = imgRGB.at<cv::Vec3b>(y_ini+idy,x_ini+idx)[1];
            cuttedRGB1.at<cv::Vec3b>(idy,idx)[2] = imgRGB.at<cv::Vec3b>(y_ini+idy,x_ini+idx)[2];
         }
    }

    QString filePartRGB = m_slOutdir.at(0) + "/1PartRGB/1PartRGB_"+ QString::number((int)code) +".jpg";
    imwrite(filePartRGB.toStdString().c_str(),cuttedRGB1);

    Size size_scale2(imgIR.cols,imgIR.rows);
    Mat cuttedRGB;
    cv::resize(cuttedRGB1, cuttedRGB, size_scale2); // cuttedRGB is 320 x 240
    Mat matmask(imgIR.rows,imgIR.cols,CV_8UC3,Scalar::all(0));

    int resaux;
    double num,dem,res;
    int countMask = 0;
    double Acumulador = 0;
    /* File for temperaturas corregidas + mascara */
    FILE *pTemperature; ///////////////
    QString filtmask = m_slOutdir.at(0) + "/3tempmask/3tempmask_"+ QString::number((int)code) +".csv";

    pTemperature = fopen(filtmask.toStdString().c_str(),"w");////////////

    for (int idy=0; idy<cuttedRGB.rows; idy++)
    {
        for (int idx=0; idx<cuttedRGB.cols; idx++)
        {
            num = cuttedRGB.at<cv::Vec3b>(idy,idx)[1] - cuttedRGB.at<cv::Vec3b>(idy,idx)[0];
            dem = cuttedRGB.at<cv::Vec3b>(idy,idx)[1] + cuttedRGB.at<cv::Vec3b>(idy,idx)[0];
            res = num/dem;
            if (std::isnan(res) || std::isinf(res))
                resaux = 0;
            else
                if (res>0){
                    resaux=1;
                    countMask++;
                }
                else
                    resaux=0;

            matmask.at<cv::Vec3b>(idy,idx)[0]=resaux*imgIR.at<cv::Vec3b>(idy,idx)[0];
            matmask.at<cv::Vec3b>(idy,idx)[1]=resaux*imgIR.at<cv::Vec3b>(idy,idx)[1];
            matmask.at<cv::Vec3b>(idy,idx)[2]=resaux*imgIR.at<cv::Vec3b>(idy,idx)[2];

            Acumulador =  Acumulador + resaux*(*(T_obj+idx+idy*imgIR.cols));
            fprintf(pTemperature,"%f,",resaux*(*(T_obj+idx+idy*imgIR.cols)));
        }
        fprintf(pTemperature,"\n");
    }

    QString fileMask1 = m_slOutdir.at(0) + "/2Mascara/2Mascara1_"+ QString::number((int)code) +".jpg";
    imwrite(fileMask1.toStdString().c_str(),matmask);

    // Date of Birth of File
    QFileInfo fi(m_slData.at(id*2));
    //QDateTime dt_fi = fi.created();
    QString StrFi(fi.created().toString("HH:mm:ss"));


    //printf("\nAcumulador: %f, countMask: %d \n",Acumulador, countMask);
    //fprintf(pFile,"%f,%f,%f,%f,%s\n",code,emi,refle,Acumulador/countMask,StrFi.toStdString().c_str());
    QString dateTimeOri;
    dateTimeOri= get_datetimeoriginal(m_slData.at(id*2));
    std::string strdTOri = dateTimeOri.toStdString().substr(45,8);

    //printf("LECTURA! : %s\n",dateTimeOri.toStdString().c_str() );
    //fprintf(pFile,"%f,%s,%f\n",code,StrFi.toStdString().c_str(),Acumulador/countMask);
    fprintf(pFile,"%f,%s,%f\n",code,strdTOri.c_str(),Acumulador/countMask);

    fclose(pTemperature);

}

    fclose(pFile);

    // Listar la carpeta de salida y mostrar imagenes.
    QString pathF0 = m_slOutdir.at(0) + "/" + path0;
    QString pathF1 = m_slOutdir.at(0) + "/" + path1;
    QString pathF2 = m_slOutdir.at(0) + "/" + path2;
    //QDir directory(m_slOutdir.at(0));

    QDir directory0(pathF0);
    QDir directory1(pathF1);
    QDir directory2(pathF2);

    QStringList filters;
    filters << "*.jpg" << "*.JPEG";

    QStringList files0;
    QStringList files1;
    QStringList files2;

    files0 = directory0.entryList(filters,QDir::Files|QDir::NoSymLinks);
    files1 = directory1.entryList(filters,QDir::Files|QDir::NoSymLinks);
    files2 = directory2.entryList(filters,QDir::Files|QDir::NoSymLinks);
    //printf("%d",files.size());

    if (files0.size()>0)
    {
        for(int i=0;i<files0.size();i++)
        {
            QString absPath = directory0.absoluteFilePath(files0.at(i));
            m_slOutfiles.append(absPath);
            ((QStringListModel*) ui->lst_outfiles->model())->setStringList(m_slOutfiles);
        }
    }

    if (files1.size()>0)
    {
        for(int i=0;i<files1.size();i++)
        {
            QString absPath = directory1.absoluteFilePath(files1.at(i));
            m_slOutfiles.append(absPath);
            ((QStringListModel*) ui->lst_outfiles->model())->setStringList(m_slOutfiles);
        }
    }

    if (files2.size()>0)
    {
        for(int i=0;i<files2.size();i++)
        {
            QString absPath = directory2.absoluteFilePath(files2.at(i));
            m_slOutfiles.append(absPath);
            ((QStringListModel*) ui->lst_outfiles->model())->setStringList(m_slOutfiles);
        }
    }
}

int Dialog::matchCodeCsv(double code)
{
    int cnt3 = 0;
    int output_mcs = 0;

    for(int id=0;id<total_entriesCSV;id++)
    {
        if (code == *(dataCSV+cnt3))
        {
            output_mcs = id+1;
            break;
        }
        cnt3 = cnt3 + 3;
    }
    return output_mcs;
}


void Dialog::on_pb_saveresults_clicked()
{

    QString dir = QFileDialog::getExistingDirectory(this,tr("Open directory"),"",QFileDialog::ShowDirsOnly|QFileDialog::DontResolveSymlinks);

    if (dir != NULL)
    {
        int cont_data = m_slOutdir.count();
        if(cont_data>0)
        {
            for(int i=0;i<cont_data;i++)
            {
                m_slOutdir.removeLast();
            }
            ((QStringListModel*) ui->lst_outdir->model())->setStringList(m_slOutdir);
        }
        m_slOutdir.append(dir);
        ((QStringListModel*) ui->lst_outdir->model())->setStringList(m_slOutdir);
    }
}


void Dialog::on_pb_addimage_2_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this,tr("Open files"),"",tr("CSV(*.csv);;All files (*.*)"));

    if (fileName != NULL)
    {
        m_sCsvfile = fileName;
        flaghito = true;

        // Reading the CSV data [ref: http://www.cplusplus.com/forum/unices/112048/]
        dataCSV = new double[300];
        total_entriesCSV = 0;
        int count_rows = 0;

        std::ifstream file(m_sCsvfile.toStdString().c_str());
        while (1){

            std::string line;
            std::getline(file, line);
            std::stringstream iss(line);
            std::string val;

            // For each line, 3 columns: 2 with comma, 1 with \n
            for (int col = 0; col < 2; ++col){
                std::getline(iss, val, ',');
                std::stringstream convertor(val);
                convertor >> dataCSV[count_rows*3+col];
            }

            std::getline(iss, val);
            std::stringstream convertor(val);
            convertor >> dataCSV[count_rows*3+2];

            total_entriesCSV += 1;
            count_rows += 1;

            if ( !file.good() )
                     break;
        }

        file.close();
    }

    //printf("%f %f %f\n",*dataCSV, *(dataCSV+1), *(dataCSV+2));
}

QString Dialog::get_datetimeoriginal(QString filename)//, char * dt_original)
{
    QProcess process1;
    QString std_out;
    QString Application = "exiftool.exe";
    QStringList Arguments;
    // 'exiftool -DateTimeOriginal ' file_imgIR
    Arguments.clear();
    Arguments.append("-DateTimeOriginal");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process1.start(Application,Arguments);
    process1.waitForFinished(-1); // will wait forever until finished
    std_out = process1.readAllStandardOutput();

    return std_out;
    //printf("LECTURA! : %s\n",std_out.toStdString().c_str() );
}



void Dialog::get_temperature(bool flag_er, QString filename ,double* emi_in, double* t_refl_in)
{
    QProcess process1; // To read file
    QProcess process2; // To read data
    QString Application = "exiftool.exe";
    QStringList Arguments;
    QString std_out;
    Mat raw;
    double PlanckB, PlanckF, PlanckO, PlanckR1, PlanckR2, Emi, T_refl;
    double RAW_refl;

    // Getting the TIFF file which be the RAW data - COMMAND 1
    // 'exiftool -b -RawThermalImage --warning  ',file_imgIR,' > temp.tiff'
    Arguments.append("-b");
    Arguments.append("-FlirImage");
    Arguments.append("-RawThermalImage");
    Arguments.append("--warning");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process1.setStandardOutputFile("test.tiff",QIODevice::Truncate);
    process1.start(Application,Arguments);
    process1.waitForFinished(-1); // will wait forever until finished


    // Reading the TIFF file
    raw = imread("test.tiff",IMREAD_UNCHANGED);

    // Reading PLANCK R1 - COMMAND 2
    // 'exiftool -b -PlanckR1 --warning ' file_imgIR
    Arguments.clear();
    Arguments.append("-b");
    Arguments.append("-PlanckR1");
    Arguments.append("--warning");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process2.start(Application,Arguments);
    process2.waitForFinished(-1); // will wait forever until finished
    std_out = process2.readAllStandardOutput();
    PlanckR1 = (double) std::atof(std_out.toStdString().c_str());
    //printf("\n%f",PlanckR1);

    // Reading PLANCK R2 - COMMAND 3
    // exiftool -b -PlanckR2 --warning ' file_imgIR
    Arguments.clear();
    Arguments.append("-b");
    Arguments.append("-PlanckR2");
    Arguments.append("--warning");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process2.start(Application,Arguments);
    process2.waitForFinished(-1); // will wait forever until finished
    std_out = process2.readAllStandardOutput();
    PlanckR2 = (double) std::atof(std_out.toStdString().c_str());
    //printf("\n%f",PlanckR2);

    // Reading PLANCK B - COMMAND 4
    // 'exiftool -b -PlanckB --warning ' file_imgIR
    Arguments.clear();
    Arguments.append("-b");
    Arguments.append("-PlanckB");
    Arguments.append("--warning");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process2.start(Application,Arguments);
    process2.waitForFinished(-1); // will wait forever until finished
    std_out = process2.readAllStandardOutput();
    PlanckB = (double) std::atof(std_out.toStdString().c_str());
    //printf("\n%f",PlanckB);

    // Reading PLANCK O - COMMAND 5
    // 'exiftool -b -PlanckO --warning ' file_imgIR
    Arguments.clear();
    Arguments.append("-b");
    Arguments.append("-PlanckO");
    Arguments.append("--warning");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process2.start(Application,Arguments);
    process2.waitForFinished(-1); // will wait forever until finished
    std_out = process2.readAllStandardOutput();
    PlanckO = (double) std::atof(std_out.toStdString().c_str());
    //printf("\n%f",PlanckO);

    // Reading PLANCK F - COMMAND 6
    //'exiftool -b -PlanckF --warning ' file_imgIR
    Arguments.clear();
    Arguments.append("-b");
    Arguments.append("-PlanckF");
    Arguments.append("--warning");
    //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
    Arguments.append(filename);
    process2.start(Application,Arguments);
    process2.waitForFinished(-1); // will wait forever until finished
    std_out = process2.readAllStandardOutput();
    PlanckF = (double) std::atof(std_out.toStdString().c_str());
    //printf("\n%f",PlanckF);

    // Reading Emissivity - COMMAND 7
    // 'exiftool -b -Emissivity --warning ' file_imgIR
    if (!flag_er)
    {
        Arguments.clear();
        Arguments.append("-b");
        Arguments.append("-Emissivity");
        Arguments.append("--warning");
        //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
        Arguments.append(filename);
        process2.start(Application,Arguments);
        process2.waitForFinished(-1); // will wait forever until finished
        std_out = process2.readAllStandardOutput();
        Emi = (double) std::atof(std_out.toStdString().c_str());
        *emi_in = Emi;
        //printf("\n%f",Emi);
    }
    else
        Emi = *emi_in;


    // Reading ReflectedApparentTemperature - COMMAND 8
    // 'exiftool -b -ReflectedApparentTemperature --warning ' file_imgIR
    if (!flag_er)
    {
        Arguments.clear();
        Arguments.append("-b");
        Arguments.append("-ReflectedApparentTemperature");
        Arguments.append("--warning");
        //Arguments.append("C:/Users/Gonzalo/Desktop/CIP2018/images/IR_8621.jpg");
        Arguments.append(filename);
        process2.start(Application,Arguments);
        process2.waitForFinished(-1); // will wait forever until finished
        std_out = process2.readAllStandardOutput();
        T_refl = (double) std::atof(std_out.toStdString().c_str());
        *t_refl_in = T_refl;
        //printf("\n%f",T_refl);
    }
    else
        T_refl = *t_refl_in;

    RAW_refl=PlanckR1/(PlanckR2*(exp(PlanckB/(T_refl+273.15))-PlanckF))-PlanckO;
    //printf("\n%f ", RAW_refl);


    double *data_raw = new double[raw.cols*raw.rows];
    double *data_raw_obj = new double[raw.cols*raw.rows];
    T_obj = new double[raw.cols*raw.rows];

    // Copying data raw (uchar) openCV -> data_raw (double) C++
    int count=0;
    for(int id_row = 0; id_row<raw.rows; id_row++)
    {
        for(int id_col = 0; id_col<raw.cols; id_col++)
        {
            *(data_raw+count) = static_cast<double> (raw.at<unsigned short>(id_row,id_col));
            count += 1;
        }
    }

    // Operation: RAW_obj=(raw -(1-Em)*RAW_refl)./Em;
    count=0;
    for(int id_row = 0; id_row<raw.rows; id_row++)
    {
        for(int id_col = 0; id_col<raw.cols; id_col++)
        {
            *(data_raw_obj+count) = (*(data_raw+count) - (1-Emi)*RAW_refl)/Emi;
            count += 1;
        }
    }
    //printf("\nDATA: %f %f %f\n", *(data_raw_obj), *(data_raw_obj+1), *(data_raw_obj+2));

    // Operation: T_obj= B ./ log(R1./(R2*(RAW_obj+O))+F) - 273.15;
    count=0;
    for(int id_row = 0; id_row<raw.rows; id_row++)
    {
        for(int id_col = 0; id_col<raw.cols; id_col++)
        {
            *(T_obj+count) = (PlanckB/(log(PlanckR1/(PlanckR2*(*(data_raw_obj+count)+PlanckO))+PlanckF)))-273.15;
            count++;
        }
    }

    //printf("\nDATA: %f %f %f\n", *(T_obj), *(T_obj+1), *(T_obj+2));
}


void Dialog::on_lst_outfiles_clicked(const QModelIndex &index)
{
    if (m_slOutfiles.count() == 0)
            return;

    QString filename;
    QPixmap pixmp;
    filename = m_slOutfiles.at(index.row());
    pixmp = QPixmap(filename);
    scene->clear();
    scene->addPixmap(pixmp);
    scene->setSceneRect(0,0,pixmp.width(),pixmp.height());
    ui->graphicsView->setScene(scene);
//    QRectF bounds = scene->itemsBoundingRect();
    ui->graphicsView->fitInView(scene->sceneRect(),Qt::IgnoreAspectRatio);
}

void Dialog::on_pb_clean_clicked()
{
    int cont_data = m_slOutfiles.count();

    if(cont_data>0)
    {
        for(int i=0;i<cont_data;i++)
        {
            m_slOutfiles.removeLast();
        }
        ((QStringListModel*) ui->lst_outfiles->model())->setStringList(m_slOutfiles);
    }

    cont_data = m_slOutdir.count();

    if(cont_data>0)
    {
        for(int i=0;i<cont_data;i++)
        {
            m_slOutdir.removeLast();
        }
        ((QStringListModel*) ui->lst_outdir->model())->setStringList(m_slOutdir);
    }

    scene->clear();

}

void Dialog::on_pb_about_clicked()
{
     AboutDlg->exec();
}
