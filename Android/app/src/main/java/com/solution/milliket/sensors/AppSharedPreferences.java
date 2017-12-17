package com.solution.milliket.sensors;

import android.content.Context;
import android.content.SharedPreferences;
import android.support.annotation.NonNull;

import java.lang.ref.WeakReference;

/**
 * Created by trannhontuan on 10/4/17.
 */

public class AppSharedPreferences {

    private static final String KEY_IP_ADDRESS  = "com.solution.milliket.sensors.KEY_IP_ADDRESS";
    private static final String KEY_PORT_NUMBER = "com.solution.milliket.sensors.KEY_PORT_NUMBER";

    private SharedPreferences mPrefs;
    private WeakReference<Context> mContext;

    public AppSharedPreferences(@NonNull Context context) {
        mContext = new WeakReference<>(context);
        mPrefs = context.getSharedPreferences(context.getPackageName(), Context.MODE_PRIVATE);
    }

    public void setIpAddress(String ipAddress) {
        mPrefs.edit().putString(KEY_IP_ADDRESS, ipAddress).apply();
    }

    public String getIpAddress() {
        return mPrefs.getString(KEY_IP_ADDRESS, "10.200.232.100");
    }

    public void setPortNumber(int portNumber) {
        mPrefs.edit().putInt(KEY_PORT_NUMBER, portNumber).apply();
    }

    public int getPortNumber() {
        return mPrefs.getInt(KEY_PORT_NUMBER, 5001);
    }
}
