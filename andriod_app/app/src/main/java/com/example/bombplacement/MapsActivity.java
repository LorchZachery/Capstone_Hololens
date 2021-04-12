package com.example.bombplacement;

import androidx.core.app.ActivityCompat;
import androidx.fragment.app.FragmentActivity;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.util.Log;
import android.util.Pair;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.*;
import java.lang.Math;
import java.text.DecimalFormat;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnSuccessListener;

import org.jetbrains.annotations.NotNull;

import java.util.Date;

import okhttp3.*;

import java.io.IOException;
import java.util.Objects;

public class MapsActivity extends FragmentActivity implements GoogleMap.OnMarkerClickListener, GoogleMap.OnMapClickListener, OnMapReadyCallback {
    //global to reload app so it does not zoom gitter
    private static boolean reload_app = true;

    //presets
    Button delete_btn;
    Button add_btn;
    Marker current_marker = null;
    LatLng current_latlon = null;
    TextView textBox;

    //giving access for fine permissions
    public static final int PERMISSION_ACCESS_FINE_LOCATION = 1;

    //hashmap to remove current locaiton mark when a new one is placed
    HashMap<Integer, Marker> hashMapMarker = new HashMap<>();
    int key = 0;


    //google map presets
    private GoogleMap mMap;
    private FusedLocationProviderClient mFusedLocationClient;
    private LocationRequest mLocationRequest;
    private LocationCallback mLocationCallback;

    //decmical formating globals
    DecimalFormat df2 = new DecimalFormat("#.##");
    DecimalFormat df6 = new DecimalFormat("#.######");

    private void startLocationUpdates() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ACCESS_FINE_LOCATION);
        }

        mFusedLocationClient.requestLocationUpdates(mLocationRequest, mLocationCallback, null);
        Toast.makeText(this, "Starting Location Updates", Toast.LENGTH_SHORT).show();
    }

    private void stopLocationUpdates() {
        mFusedLocationClient.removeLocationUpdates(mLocationCallback);
        Toast.makeText(this, "Stopping Location Updates", Toast.LENGTH_SHORT).show();
    }

    /**
     * Adds a Marker to the Map and adds the bombs()
     **/
    private void markMap(double latitude, double longitude) {

        // Add a marker at your current coordinate
        LatLng point = new LatLng(latitude, longitude);

        //removing prev current locaiton marker
        if (key != 0) {
            Marker marker = hashMapMarker.get(key - 1);
            assert marker != null;
            marker.remove();
            hashMapMarker.remove(key);
        }

        //setting current locaiton marker
        Marker marker = mMap.addMarker(new MarkerOptions()
                .position(point)
                .title("Updated:  " + new Date(System.currentTimeMillis()))
                .flat(true)
                .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE))
        );

        //adding current location marker to hash map to be removed once updated
        hashMapMarker.put(key, marker);
        key++;

        //if app is just loaded camera snaps to current location
        if (reload_app) {
            mMap.moveCamera(CameraUpdateFactory.newLatLng(point));
            reload_app = false;
        }

        //placing bombs
        getBombs(latitude, longitude);
    }

    /**
     * Sends currnet location to database
     **/
    public void sendToDB(String lat, String lon) {
        OkHttpClient httpClient = new OkHttpClient();

        RequestBody formBody = new FormBody.Builder()
                .add("lat", lat)
                .add("lon", lon)
                .build();
        Request request = new Request.Builder()
                .url("https://ied.dfcs-cloud.net/scripts/x_y.php")
                .addHeader("User-Agent", "OkHttp Bot")
                .post(formBody)
                .build();


        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                final String result = Objects.requireNonNull(response.body()).string();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                    }
                });

            }
        });
    }


    /**
     * Get bomb locations from database and place them on map and display info
     *
     * @return
     */

    public void getBombs(double currlat, double currlon) {

        OkHttpClient httpClient = new OkHttpClient();

        Activity activity = this;

        RequestBody formBody = new FormBody.Builder()
                .add("query", "SELECT lat,lon from bombs")
                .add("type", "SELECT")
                .build();

        Request request = new Request.Builder()
                .url("https://ied.dfcs-cloud.net/scripts/query.php")
                .addHeader("User-Agent", "OkHttp Bot")
                .post(formBody)
                .build();

        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();

            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                final String latlon = Objects.requireNonNull(response.body()).string();

                Log.println(Log.DEBUG, "BOMBS", latlon);

                activity.runOnUiThread(new Runnable() {
                    @SuppressLint("SetTextI18n")
                    public void run() {
                        ArrayList<Pair> bombs = parseString(latlon);

                        StringBuilder text = new StringBuilder("  Current Location: " + currlat + "," + currlon + "\n\n");

                        for (int i = 0; i < bombs.size(); i++) {
                            double lat = (double) bombs.get(i).first;
                            double lon = (double) bombs.get(i).second;

                            //getting distance form bomb
                            double distance = distance(currlat, currlon, lat, lon);

                            Log.println(Log.DEBUG, "BOMBS", "lat :" + lat + " lon: " + lon + " distance " + distance);
                            //creating text string to display information
                            text.append("   lat :").append(df6.format(lat)).append(" lon: ").append(df6.format(lon)).append("   dist: ").append(df2.format(distance)).append("m\n");

                            //adding bomb marker to map
                            LatLng point = new LatLng(lat, lon);
                            Marker marker = mMap.addMarker(new MarkerOptions().position(point)
                                    .title("Updated:  " + new Date(System.currentTimeMillis())));
                        }
                        textBox.setText(text.toString());
                    }
                });

            }

        });


    }


    public void deleteBomb(double lat, double lon) {
        OkHttpClient httpClient = new OkHttpClient();

        Activity activity = this;

        RequestBody formBody = new FormBody.Builder()
                .add("query", "DELETE FROM bombs where lat = " + lat + " and lon= " + lon)
                .add("type", "EDIT")
                .build();

        Request request = new Request.Builder()
                .url("https://ied.dfcs-cloud.net/scripts/query.php")
                .addHeader("User-Agent", "OkHttp Bot")
                .post(formBody)
                .build();
        Log.println(Log.DEBUG, "DELETE", lat + " " + lon);
        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();

            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                final String latlon = Objects.requireNonNull(response.body()).string();

                Log.println(Log.DEBUG, "DELETE", latlon);

                activity.runOnUiThread(new Runnable() {

                    public void run() {
                    }
                });
            }
        });
    }

    private void addBomb(double lat, double lon) {
        OkHttpClient httpClient = new OkHttpClient();

        Activity activity = this;

        //getting maxID to add a new bomb without overriding old entries
        RequestBody formBody = new FormBody.Builder()
                .add("query", "SELECT MAX(ID) from bombs")
                .add("type", "SELECT")
                .build();

        Request request = new Request.Builder()
                .url("https://ied.dfcs-cloud.net/scripts/query.php")
                .addHeader("User-Agent", "OkHttp Bot")
                .post(formBody)
                .build();
        Log.println(Log.DEBUG, "ADD", lat + " " + lon);
        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();

            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                final String str = Objects.requireNonNull(response.body()).string();
                String maxIDstr = str.replaceAll("[^0-9]+", "");
                int maxID = Integer.parseInt(maxIDstr) + 1;
                Log.println(Log.DEBUG, "ADD", String.valueOf(maxID));

                activity.runOnUiThread(new Runnable() {

                    public void run() {
                        executeAddBomb(lat, lon, maxID);

                    }
                });
            }
        });
    }


    private void executeAddBomb(double lat, double lon, int maxID) {
        OkHttpClient httpClient = new OkHttpClient();

        Activity activity = this;
        String query = "INSERT INTO bombs (ID, lat, lon) VALUES (" + maxID + "," + lat + "," + lon + ")";
        RequestBody formBody = new FormBody.Builder()
                .add("query", query)
                .add("type", "EDIT")
                .build();

        Request request = new Request.Builder()
                .url("https://ied.dfcs-cloud.net/scripts/query.php")
                .addHeader("User-Agent", "OkHttp Bot")
                .post(formBody)
                .build();
        Log.println(Log.DEBUG, "ADD", query);
        httpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(@NotNull Call call, @NotNull IOException e) {
                e.printStackTrace();

            }

            @Override
            public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                final String mess = Objects.requireNonNull(response.body()).string();

                Log.println(Log.DEBUG, "ADD", mess);

                activity.runOnUiThread(new Runnable() {

                    public void run() {
                        LatLng point = new LatLng(lat, lon);
                        Marker marker = mMap.addMarker(new MarkerOptions().position(point)
                                .title("Updated:  " + new Date(System.currentTimeMillis())));
                    }
                });
            }
        });
    }


    /**
     * Android Method:  Called whenever the app view is created (occurs on start and every rotation)
     **/
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setting view items
        setContentView(R.layout.activity_maps);
        delete_btn = (Button) findViewById(R.id.delete_btn);
        add_btn = (Button) findViewById(R.id.add_btn);
        textBox = (TextView) findViewById(R.id.current);


        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);

        mapFragment.getMapAsync(this);


        // Specifies how Location Data is to be Requested from the OS
        mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(500);
        mLocationRequest.setFastestInterval(200);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        LocationSettingsRequest.Builder builder = new LocationSettingsRequest.Builder().addLocationRequest(mLocationRequest);

        // Creates the Fused Location Client that will actually get the location data
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

        // Checks to Make Sure the Permissions are in Order
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ACCESS_FINE_LOCATION);
        }

        // Event Handler for when the request works (the 1st time only)
        mFusedLocationClient.getLastLocation().addOnSuccessListener(this, new OnSuccessListener() {
            @Override
            public void onSuccess(Object o) {
                if (o != null) {
                    Location l = (Location) o;
                    //Toast.makeText(this, "Getting Location Data", Toast.LENGTH_SHORT).show();
                    //markMap(l.getLatitude(), l.getLongitude());
                }
            }
        });

        // Event Handler for when the app gets program data
        mLocationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {

                for (Location location : locationResult.getLocations()) {
                    //marking map with markers of current location and bombs
                    markMap(location.getLatitude(), location.getLongitude());

                    String lat = String.valueOf(location.getLatitude());
                    String lon = String.valueOf(location.getLongitude());

                    //sending current location to database
                    sendToDB(lat, lon);
                    Log.println(Log.DEBUG, "LOCATION", "LOCATION UPDATED:  " + lat + " " + lon);
                }
            }
        };

    }

    /**
     * Android Method:  Called whenever the app comes into view
     **/
    @Override
    protected void onResume() {
        super.onResume();
        startLocationUpdates();

    }

    /**
     * Android Method:  Called whenever the app goes out of view
     **/
    @Override
    protected void onPause() {
        stopLocationUpdates();
        super.onPause();
    }

    /**
     * Event Handler for when the user responds to the request for permissions
     **/
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        switch (requestCode) {
            case PERMISSION_ACCESS_FINE_LOCATION:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this, "Fine Location Permission Granted", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(this, "Need Fine Location Permission", Toast.LENGTH_SHORT).show();
                }
                break;
        }
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        mMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);

        mMap.setOnMapClickListener(this);

        mMap.moveCamera(CameraUpdateFactory.zoomTo(15.0f));
        //zoom = false;
        googleMap.setOnInfoWindowClickListener(new GoogleMap.OnInfoWindowClickListener() {
            @Override
            public void onInfoWindowClick(Marker marker) {
            }
        });
        googleMap.setOnMarkerClickListener(new GoogleMap.OnMarkerClickListener() {
            @Override
            public boolean onMarkerClick(Marker marker) {
                Log.println(Log.DEBUG, "MARKER", marker.getTitle() + " clicked");
                delete_btn.setVisibility(View.VISIBLE);
                current_marker = marker;
                return false;
            }
        });
        googleMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
            @Override
            public void onMapClick(LatLng latLng) {
                if (add_btn.getVisibility() == View.VISIBLE) {
                    add_btn.setVisibility(View.INVISIBLE);
                    current_latlon = null;
                } else if (delete_btn.getVisibility() == View.INVISIBLE) {
                    add_btn.setVisibility(View.VISIBLE);
                    current_latlon = latLng;
                }

                delete_btn.setVisibility(View.INVISIBLE);

                Log.println(Log.DEBUG, "ADD", "touched " + latLng.latitude + " " + latLng.longitude);


            }
        });


    }


    @Override
    public boolean onMarkerClick(final Marker marker) {

        return false;
    }

    public void removeBomb(View view) {
        Log.println(Log.DEBUG, "BUTTON", "button hit");
        delete_btn.setVisibility(View.INVISIBLE);
        LatLng latlon = current_marker.getPosition();
        double lat = latlon.latitude;
        double lon = latlon.longitude;
        deleteBomb(lat, lon);
        current_marker.remove();
        current_marker = null;
        mMap.clear();

    }

    @Override
    public void onMapClick(LatLng latLng) {
        Log.println(Log.DEBUG, "MAP", "touched " + latLng.latitude + " " + latLng.longitude);
    }

    public void hidButton(View view) {
        delete_btn.setVisibility(View.INVISIBLE);
    }

    public void addBombClick(View view) {
        addBomb(current_latlon.latitude, current_latlon.longitude);
        add_btn.setVisibility(View.INVISIBLE);
    }

    /**
     * parsing string to get lat and lons from database
     * @param latlon
     * @return arraylist<Pair> of each lat lon pair
     */
    public ArrayList<Pair> parseString(String latlon) {
        String delims = "[,|{}\\[\\]\\s+\":laton\\r?\\n]";
        List<String> tokens = new ArrayList<String>(Arrays.asList(latlon.split(delims)));
        tokens.removeAll(Arrays.asList("", null));

        ArrayList<Pair> bombs = new ArrayList<>();
        for (int i = 0; i < tokens.size(); i++) {

            double lat = Double.parseDouble(tokens.get(i));
            double lon = Double.parseDouble(tokens.get(i + 1));
            i = i + 1;
            bombs.add(new Pair(lat, lon));
        }
        return bombs;
    }

    /**
     * getting distance between two coordinates
     * @param currlat
     * @param currlon
     * @param lat
     * @param lon
     * @return distance
     */
    public double distance(double currlat, double currlon, double lat, double lon) {


        //calcualte distance
        double distance = 0;
        double R = 6378100;
        double phiOne = currlat * Math.PI / 180;
        double phiTwo = lat * Math.PI / 180;
        double deltaphi = (lat - currlat) * Math.PI / 180;
        double deltarow = (lon - currlon) * Math.PI / 180;
        double a = Math.sin(deltaphi / 2) * Math.sin(deltaphi / 2) + Math.cos(phiOne) * Math.cos(phiTwo) * Math.sin(deltarow / 2) * Math.sin(deltarow / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        distance = R * c;
        return distance;
    }
}