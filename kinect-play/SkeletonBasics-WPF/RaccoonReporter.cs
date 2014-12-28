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
        private ConcurrentQueue<String> mReports = new ConcurrentQueue<String>();

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
                Report(0, 0);
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
                Thread.Sleep(5);
            }
        }


        private void doReport(){

            string report;

            Boolean isSuccess = mReports.TryDequeue(out report);
            if (!isSuccess)
            {
                return;
            }

            try
            {
                Log("Sending report: " + report);
                mSerialPort.Write(report);
            }
            catch (Exception e)
            {
                Log("Unable to write connection: " + e.StackTrace.ToString());
            }
        }

        public void Report(int lhPos, int rhPos)
        {
            // report between [0,80]
            mReports.Enqueue(lhPos+"\n");
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
