package com.solution.milliket.sensors;

import android.app.Application;

/**
 * Created by trannhontuan on 12/16/17.
 */

public class SensorApplication extends Application {

    private static AppSharedPreferences sAppSettings;
    private static SensorApplication sInstance;

    @Override
    public void onCreate() {
        super.onCreate();

        sAppSettings = new AppSharedPreferences(this);
        sInstance = this;
    }

    public static SensorApplication getInstance() {
        return sInstance;
    }

    public AppSharedPreferences getAppSettings() {
        return sAppSettings;
    }
}
