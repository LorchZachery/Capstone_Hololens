#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QString>
#include <QStringList>
#include <QStringListModel>
#include <QGraphicsScene>
#include <fstream>
#include <string>
#include <vector>
#include <QFileDialog>
#include <QFile>
#include "about.h"

namespace Ui {
class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit Dialog(QWidget *parent = 0);
    ~Dialog();

private slots:
    void on_pb_addimage_clicked();

    void on_lst_imagefile_clicked(const QModelIndex &index);

    void on_pb_deleteitem_clicked();

    void on_pb_deleteall_clicked();

    void on_pb_generate_clicked();

    void on_pb_saveresults_clicked();

    void on_pb_addimage_2_clicked();

    void get_temperature(bool flag_er,QString filename ,double* emi_in, double* t_refl_in);

    QString get_datetimeoriginal(QString filename);//, char * dt_original);

    int matchCodeCsv(double code);

    void on_lst_outfiles_clicked(const QModelIndex &index);

    void on_pb_clean_clicked();

    void on_pb_about_clicked();

private:
    Ui::Dialog *ui;
    QStringList m_slData;
    QGraphicsScene *scene;
    QStringList m_slOutfiles;
    QStringList m_slOutdir;
    QString m_sCsvfile;
    bool flaghito;
    double *dataCSV;
    int total_entriesCSV;
    double* T_obj;
    about* AboutDlg;

};

#endif // DIALOG_H
