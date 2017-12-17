package com.solution.milliket.sensors;

/**
 * Created by trannhontuan on 12/16/17.
 */

public interface OnServerFeedbackListener {

    void onReceiveMessage(String msg);

    void onLastAction(String action);

}
