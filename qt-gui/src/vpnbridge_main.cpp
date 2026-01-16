#include "MainWindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName("SoftEther VPN Bridge");
    MainWindow w;
    w.setWindowTitle("SoftEther VPN Bridge");
    w.show();
    return app.exec();
}
