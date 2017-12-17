package com.solution.milliket.sensors;

/**
 * Created by trannhontuan on 12/15/17.
 */

public class SensorVal {

    private String type;
    private Values values;

    public SensorVal() {

    }

    public SensorVal(String type, Values values) {
        super();
        this.type = type;
        this.values = values;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Values getValues() {
        return values;
    }

    public void setValues(Values values) {
        this.values = values;
    }

    public static class Values {

        private float x;
        private float y;
        private float z;

        public Values() {

        }

        public Values(float x, float y, float z) {
            super();
            this.x = x;
            this.y = y;
            this.z = z;
        }

        public float getX() {
            return x;
        }

        public void setX(float x) {
            this.x = x;
        }

        public float getY() {
            return y;
        }

        public void setY(float y) {
            this.y = y;
        }

        public float getZ() {
            return z;
        }

        public void setZ(float z) {
            this.z = z;
        }

    }

}
