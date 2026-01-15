#include "MainWindow.h"
#include <QMenuBar>
#include <QToolBar>
#include <QStatusBar>
#include <QIcon>
#include <QLabel>






MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("SoftEther VPN Manager (Qt)");
    setMinimumSize(900, 600);

    // Load icons from Qt resource system
    QIcon vpnIcon(":/icons/VPN.ico");
    QIcon serverIcon(":/icons/Server.ico");
    QIcon serverOfflineIcon(":/icons/Server_Offline.ico");

    // Menu bar
    QMenuBar *menuBar = new QMenuBar(this);
    setMenuBar(menuBar);
    QMenu *fileMenu = menuBar->addMenu("&File");
    QMenu *accountMenu = menuBar->addMenu("&Account");
    QMenu *adapterMenu = menuBar->addMenu("&Virtual Adapter");
    menuBar->addMenu("&Tools");
    menuBar->addMenu("&Help");

    // Account actions
    addAccountAction = new QAction(vpnIcon, "Add Account", this);
    editAccountAction = new QAction(vpnIcon, "Edit Account", this);
    importAccountsAction = new QAction(serverIcon, "Import Accounts...", this);
    exportAccountsAction = new QAction(serverIcon, "Export Accounts...", this);
    accountMenu->addAction(addAccountAction);
    accountMenu->addAction(editAccountAction);
    accountMenu->addSeparator();
    accountMenu->addAction(importAccountsAction);
    accountMenu->addAction(exportAccountsAction);
    connect(addAccountAction, &QAction::triggered, this, &MainWindow::onAddAccount);
    connect(editAccountAction, &QAction::triggered, this, &MainWindow::onEditAccount);
    connect(importAccountsAction, &QAction::triggered, this, &MainWindow::onImportAccounts);
    connect(exportAccountsAction, &QAction::triggered, this, &MainWindow::onExportAccounts);

    // VLAN management actions
    manageVLANAction = new QAction(serverIcon, "Manage VLANs", this);
    importVLANsAction = new QAction(serverIcon, "Import VLANs...", this);
    exportVLANsAction = new QAction(serverIcon, "Export VLANs...", this);
    adapterMenu->addAction(manageVLANAction);
    adapterMenu->addSeparator();
    adapterMenu->addAction(importVLANsAction);
    adapterMenu->addAction(exportVLANsAction);
    connect(manageVLANAction, &QAction::triggered, this, &MainWindow::onManageVLAN);
    connect(importVLANsAction, &QAction::triggered, this, &MainWindow::onImportVLANs);
    connect(exportVLANsAction, &QAction::triggered, this, &MainWindow::onExportVLANs);

    // Status action
    showStatusAction = new QAction(serverOfflineIcon, "Show Status", this);
    accountMenu->addAction(showStatusAction);
    connect(showStatusAction, &QAction::triggered, this, &MainWindow::onShowStatus);

    // Toolbar
    QToolBar *toolBar = new QToolBar(this);
    addToolBar(toolBar);
    QAction *newAction = toolBar->addAction(vpnIcon, "New");
    QAction *editAction = toolBar->addAction(vpnIcon, "Edit");
    QAction *vlanAction = toolBar->addAction(serverIcon, "VLAN");
    QAction *statusAction = toolBar->addAction(serverOfflineIcon, "Status");
    QAction *importAccAction = toolBar->addAction(serverIcon, "Import Acc");
    QAction *exportAccAction = toolBar->addAction(serverIcon, "Export Acc");
    QAction *importVlanAction = toolBar->addAction(serverIcon, "Import VLAN");
    QAction *exportVlanAction = toolBar->addAction(serverIcon, "Export VLAN");
    toolBar->addAction(QIcon(), "Delete");
    toolBar->addSeparator();
    toolBar->addAction(QIcon(), "Connect");
    toolBar->addAction(QIcon(), "Disconnect");
    toolBar->addSeparator();
    toolBar->addAction(QIcon(), "Refresh");
    connect(newAction, &QAction::triggered, this, &MainWindow::onAddAccount);
    connect(editAction, &QAction::triggered, this, &MainWindow::onEditAccount);
    connect(vlanAction, &QAction::triggered, this, &MainWindow::onManageVLAN);
    connect(statusAction, &QAction::triggered, this, &MainWindow::onShowStatus);
    connect(importAccAction, &QAction::triggered, this, &MainWindow::onImportAccounts);
    connect(exportAccAction, &QAction::triggered, this, &MainWindow::onExportAccounts);
    connect(importVlanAction, &QAction::triggered, this, &MainWindow::onImportVLANs);
    connect(exportVlanAction, &QAction::triggered, this, &MainWindow::onExportVLANs);

    // Status bar
    QStatusBar *statusBar = new QStatusBar(this);
    setStatusBar(statusBar);
    statusBar->showMessage("Ready");

    // Central widget placeholder
    QLabel *label = new QLabel("SoftEther VPN Qt GUI Placeholder\n(Integrate your logic here)", this);
    label->setAlignment(Qt::AlignCenter);
    setCentralWidget(label);
}





MainWindow::~MainWindow() {}

void MainWindow::onAddAccount() {
    AccountDialog dlg(this);
    if (dlg.exec() == QDialog::Accepted) {
        QVariantMap data = dlg.accountData();
        // TODO: Add account to model/backend
    }
}

void MainWindow::onEditAccount() {
    AccountDialog dlg(this);
    // TODO: Load selected account data into dialog
    // dlg.setAccountData(selectedAccountData);
    if (dlg.exec() == QDialog::Accepted) {
        QVariantMap data = dlg.accountData();
        // TODO: Update account in model/backend
    }
}

void MainWindow::onManageVLAN() {
    VLANDialog dlg(this);
    // TODO: Load VLAN data from backend
    // dlg.setVLANData(vlanList);
    if (dlg.exec() == QDialog::Accepted) {
        QVariantList vlans = dlg.vlanData();
        // TODO: Save VLAN data to backend
    }
}


void MainWindow::onShowStatus() {
    // For demo, use first account name or a placeholder
    QString accountName = "default";
    static VpnBackend backend;
    StatusDialog dlg(&backend, accountName, this);
    dlg.exec();
}

void MainWindow::onImportAccounts() {
    // TODO: Implement import logic for accounts (e.g., QFileDialog, parse file, update model)
}

void MainWindow::onExportAccounts() {
    // TODO: Implement export logic for accounts (e.g., QFileDialog, write file from model)
}

void MainWindow::onImportVLANs() {
    // TODO: Implement import logic for VLANs (e.g., QFileDialog, parse file, update model)
}

void MainWindow::onExportVLANs() {
    // TODO: Implement export logic for VLANs (e.g., QFileDialog, write file from model)
}
