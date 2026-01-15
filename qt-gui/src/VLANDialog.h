#pragma once
#include <QDialog>
#include <QLineEdit>
#include <QComboBox>
#include <QCheckBox>
#include <QTableWidget>
#include <QDialogButtonBox>

class VLANDialog : public QDialog {
    Q_OBJECT
public:
    VLANDialog(QWidget *parent = nullptr);
    void setVLANData(const QVariantList &vlans);
    QVariantList vlanData() const;
private:
    QTableWidget *vlanTable;
    QDialogButtonBox *buttonBox;
    void setupUi();
};
