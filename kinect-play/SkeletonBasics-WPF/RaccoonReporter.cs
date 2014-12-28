using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO.Ports;
using System.IO;
using System.Threading;
using System.ComponentModel;
using System.Collections.Concurrent;

namespace Microsoft.Samples.Kinect.SkeletonBasics
{
    class RaccoonReporter
    {
        private SerialPort mSerialPort;
        private String mLatestReport;
        private volatile Boolean mShouldReport;

        public void Open(){
            mSerialPort = new System.IO.Ports.SerialPort("COM11");
            mSerialPort.BaudRate = 9600;
            mSerialPort.StopBits = StopBits.One;
            mSerialPort.DataBits = 8;
            mSerialPort.Parity = Parity.None;
            mSerialPort.Handshake = Handshake.None;

            try
            {
                mSerialPort.Open();
                RequestReport(0, 0);
            }
            catch (Exception e)
            {
                Log("Unable to open connection: " + e.StackTrace.ToString());
            }

            if (mSerialPort.IsOpen)
            {
                Log("Serial connection opened");
            }
            else
            {
                Log("Unable to open conneciton");
            }
            Thread thread = new Thread(ReporterLoop);
            thread.Start();
        }

        public void ReporterLoop()
        {
            Log("ReporterLoop started");
            while (true)
            {
                doReport();
                Thread.Sleep(2);
            }
        }

        public void RequestReport(int lhPos, int rhPos)
        {
            // report between [0,80]
            string report = lhPos + "\n";
            if (!report.Equals(mLatestReport))
            {
                mLatestReport = report;
                mShouldReport = true;
            }
        }

        private void doReport(){

            if (!mShouldReport)
            {
                return;
            }
        
            try
            {
                Log("Sending report: " + mLatestReport);
                if (mSerialPort.IsOpen)
                {
                    mSerialPort.Write(mLatestReport);
                }
                mShouldReport = false;
            }
            catch (Exception e)
            {
                Log("Unable to write connection: " + e.StackTrace.ToString());
            }
        }

        public void Close(){
            try
            {
                mSerialPort.Close();
            }
            catch (Exception e)
            {
                Log("Unable to close connection: " + e.StackTrace.ToString());
                Log("Serial connection closed.");
            }
            
        }

        private void Log(string msg)
        {
            MainWindow.Log(msg);
        }

    }
}
