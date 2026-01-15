#pragma once
#include <QMainWindow>




#include "AccountDialog.h"
#include "VLANDialog.h"
#include "StatusDialog.h"




class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onAddAccount();
    void onEditAccount();
    void onManageVLAN();
    void onShowStatus();
    void onImportAccounts();
    void onExportAccounts();
    void onImportVLANs();
    void onExportVLANs();

private:
    QAction *addAccountAction;
    QAction *editAccountAction;
    QAction *manageVLANAction;
    QAction *showStatusAction;
    QAction *importAccountsAction;
    QAction *exportAccountsAction;
    QAction *importVLANsAction;
    QAction *exportVLANsAction;
};
