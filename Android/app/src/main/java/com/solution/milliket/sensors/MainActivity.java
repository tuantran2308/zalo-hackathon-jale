package com.solution.milliket.sensors;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Handler;
import android.os.Looper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import java.util.Locale;

import static android.hardware.Sensor.TYPE_ACCELEROMETER;

public class MainActivity extends AppCompatActivity implements SensorEventListener, View.OnClickListener, OnServerFeedbackListener {

    public static final int SAMPLE_RATE = 50;
    public static final String COMMAND_PLAY = "play";

    private static final String FORMAT_X = "x: %.5f";
    private static final String FORMAT_Y = "y: %.5f";
    private static final String FORMAT_Z = "z: %.5f";
    private static final String FORMAT_XYZ = "(%.5f, %.5f, %.5f)";
    private static final String FORMAT_STATUS = "Status: %s";
    private static final String FORMAT_ACTION = "Last Action: %s";

    private TextView mAccXyz;
    private TextView mStatusTv;
    private TextView mLastActionTv;

    private EditText mServerIpAddressEdt, mServerPortEdt;
    private Button mConnectBtn, mPlayBtn;

    private SensorManager mSensorManager;
    private Sensor mAccelerometer;

    private CommunicateThread mCommunicateThread;
    private Gson mGson;

    private Handler mHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mAccXyz = findViewById(R.id.acc_xyz);
        mStatusTv = findViewById(R.id.tv_status);
        mLastActionTv = findViewById(R.id.tv_last_action);

        mServerIpAddressEdt = findViewById(R.id.edt_ip);
        mServerPortEdt = findViewById(R.id.edt_port);
        mConnectBtn = findViewById(R.id.btn_connect);

        mServerIpAddressEdt.setText(SensorApplication.getInstance().getAppSettings().getIpAddress());
        mServerPortEdt.setText(String.valueOf(SensorApplication.getInstance().getAppSettings().getPortNumber()));

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        if (mSensorManager != null) {
            mAccelerometer = mSensorManager.getDefaultSensor(TYPE_ACCELEROMETER);
            if (mAccelerometer == null) {
                Toast.makeText(this, "This device does not support accelerometer sensor", Toast.LENGTH_SHORT).show();
            }
        }

        mConnectBtn.setOnClickListener(this);

        mGson = new Gson();

        mHandler = new Handler(Looper.getMainLooper());

    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.btn_connect:
                String ip = mServerIpAddressEdt.getText().toString();
                int port = Integer.parseInt(mServerPortEdt.getText().toString());

                if (mCommunicateThread != null) {
                    mCommunicateThread.close();
                }

                mCommunicateThread = new CommunicateThread(ip, port);
                mCommunicateThread.setOnServerCommanListener(this);
                mCommunicateThread.start();

                AppSharedPreferences appSettings = SensorApplication.getInstance().getAppSettings();
                if (appSettings != null) {
                    appSettings.setIpAddress(ip);
                    appSettings.setPortNumber(port);
                }
                break;

//            case R.id.btn_play:
//                if (mCommunicateThread != null && mGson != null) {
//                    SensorVal sensorVal = new SensorVal();
//                    sensorVal.setType("test_play");
//                    SensorVal.Values values = new SensorVal.Values(0.0f, 0.0f, 0.0f);
//                    sensorVal.setValues(values);
//                    mCommunicateThread.sendSomeThing(mGson.toJson(sensorVal));
//                }

            default:
                break;
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (mSensorManager != null) {
            if (mAccelerometer != null) {
                mSensorManager.registerListener(this, mAccelerometer, SensorManager.SENSOR_DELAY_FASTEST);
            }
        }
    }

    @Override
    protected void onPause() {
        super.onPause();

        if (mSensorManager != null) {
            if (mAccelerometer != null) {
                mSensorManager.unregisterListener(this);
            }
        }
    }

    private long mLastTime;

    @Override
    public void onSensorChanged(SensorEvent event) {
        Sensor sensor = event.sensor;
        if (sensor == null) {
            return;
        }

        float ox = event.values[0];
        float oy = event.values[1];
        float oz = event.values[2];
        SensorVal.Values values = new SensorVal.Values(ox, oy, oz);
        SensorVal val = new SensorVal();
        val.setValues(values);

        int type = sensor.getType();
        if (TYPE_ACCELEROMETER == type) {

            mAccXyz.setText(String.format(Locale.US, FORMAT_XYZ, ox, oy, oz));

            long curr = System.currentTimeMillis();
            if (curr - mLastTime >= SAMPLE_RATE) {
                mLastTime = curr;

                val.setType("acc");
                if (mCommunicateThread != null) {
                    mCommunicateThread.sendSomeThing(mGson.toJson(val));
                }
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    protected void onDestroy() {
        if (mCommunicateThread != null) {
            mCommunicateThread.close();
            mCommunicateThread = null;
        }

        super.onDestroy();
    }

    @Override
    public void onReceiveMessage(final String msg) {
        if (mHandler != null) {
            mHandler.post(new Runnable() {
                @Override
                public void run() {
                    if (mStatusTv != null) {
                        mStatusTv.setText(String.format(FORMAT_STATUS, msg));
                    }
                }
            });
        }
    }

    @Override
    public void onLastAction(final String action) {
        if (mHandler != null) {
            mHandler.post(new Runnable() {
                @Override
                public void run() {
                    if (mLastActionTv != null) {
                        mLastActionTv.setText(String.format(FORMAT_ACTION, action));
                    }
                }
            });
        }
    }
}
