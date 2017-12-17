package com.solution.milliket.sensors;

import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * Created by trannhontuan on 12/15/17.
 */

public class CommunicateThread extends Thread {

    public static final String MODE_ALL = "mode_all";
    public static final String MODE_PRESENT = "mode_present";
    public static final String MODE_CONTINUOUS = "mode_continuous";

    public static final String ACTION_LOCK = "action_lock";
    public static final String ACTION_UNLOCK = "action_unlock";
    public static final String ACTION_PUNCH = "action_punch";
    public static final String ACTION_HOOK = "action_hook";
    public static final String ACTION_NEXT = "action_next";
    public static final String ACTION_PREV = "action_prev";

    String dstAddress;
    int dstPort;
    private Socket mSocket;
    private OutputStream outputStream;
    private OutputStreamWriter writer;

    private OnServerFeedbackListener mServerCmdListener;

    public CommunicateThread(String dstAddress, int dstPort) {
        this.dstAddress = dstAddress;
        this.dstPort = dstPort;
    }

    public void setOnServerCommanListener(OnServerFeedbackListener listener) {
        mServerCmdListener = listener;
    }

    @Override
    public void run() {
        super.run();

        try {
            mSocket = new Socket(dstAddress, dstPort);

            char[] buffer = new char[1024];

            int bytesRead;
            InputStream inputStream = mSocket.getInputStream();
            InputStreamReader reader = new InputStreamReader(inputStream);

            while (true) {

                if ((bytesRead = reader.read(buffer)) != -1) {

                    String msg = new String(buffer, 0, bytesRead);
                    Log.d("TUAN_DEBUG", "#run: receive: " + msg);

                    if (mServerCmdListener != null) {
                        if (MODE_ALL.equals(msg)) {
                            mServerCmdListener.onReceiveMessage("Mode All");

                        } else if (MODE_PRESENT.equals(msg)) {
                            mServerCmdListener.onReceiveMessage("Mode Presentation");

                        } else if (MODE_CONTINUOUS.equals(msg)) {
                            mServerCmdListener.onReceiveMessage("Mode Continuous");

                        } else if (ACTION_LOCK.equals(msg)) {
                            mServerCmdListener.onLastAction("Lock");

                        } else if (ACTION_UNLOCK.equals(msg)) {
                            mServerCmdListener.onLastAction("Unlock");

                        } else if (ACTION_PUNCH.equals(msg)) {
                            mServerCmdListener.onLastAction("Punch");

                        } else if (ACTION_HOOK.equals(msg)) {
                            mServerCmdListener.onLastAction("Hook");

                        } else if (ACTION_NEXT.equals(msg)) {
                            mServerCmdListener.onLastAction("Next");

                        } else if (ACTION_PREV.equals(msg)) {
                            mServerCmdListener.onLastAction("Prev");

                        }
                    }


//                    Handler handler = new Handler(Looper.getMainLooper());
//                    handler.post(new Runnable() {
//                        @Override
//                        public void run() {
//                            textResponse.setText(response);
//                        }
//                    });
                }
            }

        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            close();
        }
    }

    public void close() {
        Log.d("TUAN_DEBUG", "#close");
        if (mSocket != null && !mSocket.isClosed()) {
            try {
                mSocket.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    public void sendSomeThing(final String s) {

//        Log.d("TUAN_DEBUG", "#sendSomeThing: " + s);

        if (mSocket != null && !mSocket.isClosed()) {

            try {
                if (outputStream == null) {
                    outputStream = mSocket.getOutputStream();
                }
                if (writer == null) {
                    writer = new OutputStreamWriter(outputStream, "UTF-8");
                }

                writer.write(s, 0, s.length());
                writer.flush();


//                Handler handler = new Handler(Looper.getMainLooper());
//                handler.post(new Runnable() {
//                    @Override
//                    public void run() {
//                        textResponse.setText(s);
//                    }
//                });

            } catch (IOException e) {
                e.printStackTrace();
                close();
            }

        } else {
            Log.d("TUAN_DEBUG", "#sendSomeThing: closed");
        }
    }
}
