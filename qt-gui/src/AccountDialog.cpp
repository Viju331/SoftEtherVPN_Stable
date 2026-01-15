#include "AccountDialog.h"
#include <QVBoxLayout>
#include <QFormLayout>
#include <QLabel>

AccountDialog::AccountDialog(QWidget *parent) : QDialog(parent) {
    setupUi();
}

void AccountDialog::setupUi() {
    setWindowTitle("VPN Connection Settings");
    resize(500, 400);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    tabWidget = new QTabWidget(this);
    // General tab
    QWidget *generalTab = new QWidget;
    QFormLayout *generalLayout = new QFormLayout(generalTab);
    nameEdit = new QLineEdit;
    serverEdit = new QLineEdit;
    portEdit = new QLineEdit;
    hubEdit = new QLineEdit;
    adapterCombo = new QComboBox;
    startupCheck = new QCheckBox("Connect at startup");
    generalLayout->addRow("Connection Name:", nameEdit);
    generalLayout->addRow("Server:", serverEdit);
    generalLayout->addRow("Port:", portEdit);
    generalLayout->addRow("Virtual HUB:", hubEdit);
    generalLayout->addRow("Adapter:", adapterCombo);
    generalLayout->addRow(startupCheck);
    tabWidget->addTab(generalTab, "General");
    // Auth tab
    QWidget *authTab = new QWidget;
    QFormLayout *authLayout = new QFormLayout(authTab);
    authTypeCombo = new QComboBox;
    authTypeCombo->addItems({"Password", "Certificate", "RADIUS", "NT Domain", "Anonymous"});
    usernameEdit = new QLineEdit;
    passwordEdit = new QLineEdit;
    passwordEdit->setEchoMode(QLineEdit::Password);
    authLayout->addRow("Auth Type:", authTypeCombo);
    authLayout->addRow("Username:", usernameEdit);
    authLayout->addRow("Password:", passwordEdit);
    tabWidget->addTab(authTab, "Authentication");
    // Advanced tab
    QWidget *advTab = new QWidget;
    QFormLayout *advLayout = new QFormLayout(advTab);
    tcpConnEdit = new QLineEdit;
    timeoutEdit = new QLineEdit;
    halfConnCheck = new QCheckBox("Half-Duplex");
    udpAccelCheck = new QCheckBox("UDP Acceleration");
    compressCheck = new QCheckBox("Compression");
    bridgeCheck = new QCheckBox("Bridge Mode");
    monitorCheck = new QCheckBox("Monitor Mode");
    cipherCombo = new QComboBox;
    cipherCombo->addItems({"AES-128", "AES-256", "ChaCha20", "RC4"});
    advLayout->addRow("TCP Connections:", tcpConnEdit);
    advLayout->addRow("Timeout:", timeoutEdit);
    advLayout->addRow(halfConnCheck);
    advLayout->addRow(udpAccelCheck);
    advLayout->addRow(compressCheck);
    advLayout->addRow(bridgeCheck);
    advLayout->addRow(monitorCheck);
    advLayout->addRow("Cipher:", cipherCombo);
    tabWidget->addTab(advTab, "Advanced");
    // Proxy tab
    QWidget *proxyTab = new QWidget;
    QFormLayout *proxyLayout = new QFormLayout(proxyTab);
    proxyTypeCombo = new QComboBox;
    proxyTypeCombo->addItems({"Direct", "HTTP", "SOCKS"});
    proxyHostEdit = new QLineEdit;
    proxyPortEdit = new QLineEdit;
    proxyUserEdit = new QLineEdit;
    proxyPassEdit = new QLineEdit;
    proxyPassEdit->setEchoMode(QLineEdit::Password);
    proxyLayout->addRow("Proxy Type:", proxyTypeCombo);
    proxyLayout->addRow("Host:", proxyHostEdit);
    proxyLayout->addRow("Port:", proxyPortEdit);
    proxyLayout->addRow("User:", proxyUserEdit);
    proxyLayout->addRow("Password:", proxyPassEdit);
    tabWidget->addTab(proxyTab, "Proxy");
    // Buttons
    buttonBox = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, this);
    mainLayout->addWidget(tabWidget);
    mainLayout->addWidget(buttonBox);
    connect(buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
    connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
}

void AccountDialog::setAccountData(const QVariantMap &data) {
    nameEdit->setText(data.value("AccountName").toString());
    serverEdit->setText(data.value("ServerName").toString());
    portEdit->setText(data.value("Port").toString());
    hubEdit->setText(data.value("HubName").toString());
    adapterCombo->setCurrentText(data.value("DeviceName").toString());
    startupCheck->setChecked(data.value("StartupAccount").toBool());
    authTypeCombo->setCurrentText(data.value("AuthType").toString());
    usernameEdit->setText(data.value("Username").toString());
    passwordEdit->setText(data.value("Password").toString());
    tcpConnEdit->setText(data.value("TCPConnections").toString());
    timeoutEdit->setText(data.value("Timeout").toString());
    halfConnCheck->setChecked(data.value("HalfConnection").toBool());
    udpAccelCheck->setChecked(data.value("UDPAcceleration").toBool());
    compressCheck->setChecked(data.value("Compression").toBool());
    bridgeCheck->setChecked(data.value("BridgeMode").toBool());
    monitorCheck->setChecked(data.value("MonitorMode").toBool());
    cipherCombo->setCurrentText(data.value("Cipher").toString());
    proxyTypeCombo->setCurrentText(data.value("ProxyType").toString());
    proxyHostEdit->setText(data.value("ProxyHost").toString());
    proxyPortEdit->setText(data.value("ProxyPort").toString());
    proxyUserEdit->setText(data.value("ProxyUser").toString());
    proxyPassEdit->setText(data.value("ProxyPassword").toString());
}

QVariantMap AccountDialog::accountData() const {
    QVariantMap data;
    data["AccountName"] = nameEdit->text();
    data["ServerName"] = serverEdit->text();
    data["Port"] = portEdit->text();
    data["HubName"] = hubEdit->text();
    data["DeviceName"] = adapterCombo->currentText();
    data["StartupAccount"] = startupCheck->isChecked();
    data["AuthType"] = authTypeCombo->currentText();
    data["Username"] = usernameEdit->text();
    data["Password"] = passwordEdit->text();
    data["TCPConnections"] = tcpConnEdit->text();
    data["Timeout"] = timeoutEdit->text();
    data["HalfConnection"] = halfConnCheck->isChecked();
    data["UDPAcceleration"] = udpAccelCheck->isChecked();
    data["Compression"] = compressCheck->isChecked();
    data["BridgeMode"] = bridgeCheck->isChecked();
    data["MonitorMode"] = monitorCheck->isChecked();
    data["Cipher"] = cipherCombo->currentText();
    data["ProxyType"] = proxyTypeCombo->currentText();
    data["ProxyHost"] = proxyHostEdit->text();
    data["ProxyPort"] = proxyPortEdit->text();
    data["ProxyUser"] = proxyUserEdit->text();
    data["ProxyPassword"] = proxyPassEdit->text();
    return data;
}
