#include "VLANDialog.h"
#include <QVBoxLayout>
#include <QHeaderView>

VLANDialog::VLANDialog(QWidget *parent) : QDialog(parent) {
    setupUi();
}

void VLANDialog::setupUi() {
    setWindowTitle("Virtual LAN (VLAN) Management");
    resize(600, 400);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    vlanTable = new QTableWidget(this);
    vlanTable->setColumnCount(3);
    vlanTable->setHorizontalHeaderLabels({"VLAN ID", "Name", "Enabled"});
    vlanTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    vlanTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    vlanTable->setEditTriggers(QAbstractItemView::DoubleClicked | QAbstractItemView::EditKeyPressed);
    buttonBox = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, this);
    mainLayout->addWidget(vlanTable);
    mainLayout->addWidget(buttonBox);
    connect(buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
    connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
}

void VLANDialog::setVLANData(const QVariantList &vlans) {
    vlanTable->setRowCount(vlans.size());
    for (int i = 0; i < vlans.size(); ++i) {
        QVariantMap vlan = vlans[i].toMap();
        vlanTable->setItem(i, 0, new QTableWidgetItem(vlan.value("VLANID").toString()));
        vlanTable->setItem(i, 1, new QTableWidgetItem(vlan.value("Name").toString()));
        QTableWidgetItem *enabledItem = new QTableWidgetItem;
        enabledItem->setCheckState(vlan.value("Enabled").toBool() ? Qt::Checked : Qt::Unchecked);
        vlanTable->setItem(i, 2, enabledItem);
    }
}

QVariantList VLANDialog::vlanData() const {
    QVariantList vlans;
    for (int i = 0; i < vlanTable->rowCount(); ++i) {
        QVariantMap vlan;
        vlan["VLANID"] = vlanTable->item(i, 0)->text();
        vlan["Name"] = vlanTable->item(i, 1)->text();
        vlan["Enabled"] = vlanTable->item(i, 2)->checkState() == Qt::Checked;
        vlans.append(vlan);
    }
    return vlans;
}
