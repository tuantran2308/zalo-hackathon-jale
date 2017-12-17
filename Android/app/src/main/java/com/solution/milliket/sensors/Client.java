package com.solution.milliket.sensors;

import android.os.AsyncTask;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.widget.TextView;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client extends AsyncTask<Void, String, Void> {

	String dstAddress;
	int dstPort;
	String response = "";
	TextView textResponse;
	private Socket mSocket;

	Client(String addr, int port, TextView textResponse) {
		dstAddress = addr;
		dstPort = port;
		this.textResponse=textResponse;
	}

	@Override
	protected Void doInBackground(Void... arg0) {

		mSocket = null;

		try {
			mSocket = new Socket(dstAddress, dstPort);

			ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(
					1024);
			byte[] buffer = new byte[1024];

			int bytesRead;
			InputStream inputStream = mSocket.getInputStream();

            Log.d("TUAN_DEBUG", "#while (true) {");
            while (true) {

                Log.d("TUAN_DEBUG", "if ((bytesRead = inputStream.read(buffer)) != -1) {");
                if ((bytesRead = inputStream.read(buffer)) != -1) {
                    byteArrayOutputStream.write(buffer, 0, bytesRead);
                    response += byteArrayOutputStream.toString("UTF-8");

                    Handler handler = new Handler(Looper.getMainLooper());
                    handler.post(new Runnable() {
                        @Override
                        public void run() {
                            textResponse.setText(response);
                        }
                    });
                }
            }

		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			response = "UnknownHostException: " + e.toString();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			response = "IOException: " + e.toString();
		} catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } finally {
            Log.d("TUAN_DEBUG", "finally");
			if (mSocket != null) {
				try {
					mSocket.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		return null;
	}

	@Override
	protected void onPostExecute(Void result) {
        super.onPostExecute(result);
	}

    @Override
    protected void onProgressUpdate(String... values) {
        super.onProgressUpdate(values);
    }

    public void sendSomeThing(final String s) {

        Log.d("TUAN_DEBUG", "#sendSomeThing");

        if (mSocket != null && !mSocket.isClosed()) {
			OutputStream outputStream;

			try {
				outputStream = mSocket.getOutputStream();
				PrintStream printStream = new PrintStream(outputStream);
				printStream.print(s);
				printStream.flush();

                Handler handler = new Handler(Looper.getMainLooper());
                handler.post(new Runnable() {
                    @Override
                    public void run() {
                        textResponse.setText(s);
                    }
                });

			} catch (IOException e) {
				e.printStackTrace();
			}

		} else {
            Log.d("TUAN_DEBUG", "#sendSomeThing: closed");
        }
	}

}
