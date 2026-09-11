package com.standingwater.facsimile;

import android.os.Bundle;
import android.view.View;

import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;

import com.getcapacitor.BridgeActivity;

/**
 * The book, full bleed.
 *
 * Android 15 and up force apps edge-to-edge and ignore the old fullscreen
 * window flags, so the status and navigation bars have to be hidden through
 * the insets controller instead. BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE means
 * a swipe from an edge shows them for a moment and then they withdraw — which
 * matters here, because the page turn is itself an edge swipe and a reader who
 * summoned the navigation bar every time they turned a leaf would stop
 * turning leaves.
 *
 * The bars are re-hidden on every return to focus. Android puts them back
 * after a dialog, an app switch, or the screen locking, and without this the
 * book would quietly acquire a status bar partway through the evening.
 */
public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Before super.onCreate: the bridge is built there, and a plugin
        // registered afterwards is not in it.
        registerPlugin(BooksPlugin.class);
        super.onCreate(savedInstanceState);
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        hideSystemBars();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            hideSystemBars();
        }
    }

    private void hideSystemBars() {
        View decor = getWindow().getDecorView();
        WindowInsetsControllerCompat c =
                WindowCompat.getInsetsController(getWindow(), decor);
        c.setSystemBarsBehavior(
                WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        c.hide(WindowInsetsCompat.Type.systemBars());
    }
}
