package com.standingwater.facsimile;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;

/**
 * Finds book bundles that were added to the tablet.
 *
 * The WebView is served from https://localhost and cannot read /sdcard, so
 * something native has to enumerate the books and hand back their manifests.
 * That is all this does: list the directories under the app's own external
 * files folder that contain a book.json, and return each one's text plus its
 * absolute path. The web side turns that path into a loadable URL with
 * Capacitor.convertFileSrc, so page images stay ordinary <img src> streamed by
 * the native layer — no base64, and no second copy of the book in memory.
 *
 * This exists instead of @capacitor/filesystem, which is a far larger
 * dependency for three operations and which declares a Kotlin jvmToolchain of
 * 21 — a hard requirement for a JDK that is not installed on this machine,
 * where the only options are 17 and a 25 that Gradle 8.14 refuses to run on.
 * Sixty lines of plain Java compile at 17 with everything else and add no
 * dependency at all.
 *
 * The directory used is getExternalFilesDir(), which needs no storage
 * permission and is visible over USB and in My Files, so a book can be dropped
 * in by hand. It is also removed when the app is uninstalled, which is the
 * correct behaviour for content the app is the reader of.
 */
@CapacitorPlugin(name = "Books")
public class BooksPlugin extends Plugin {

    private File booksDir() {
        File ext = getContext().getExternalFilesDir(null);
        if (ext == null) return null;
        File books = new File(ext, "books");
        // Created eagerly so there is always a real folder to drop a book
        // into, rather than a path the reader has to type from memory.
        if (!books.exists() && !books.mkdirs()) return books;
        return books;
    }

    /** java.nio.file is API 26; minSdk here is 24. */
    private static String readText(File f) throws IOException {
        try (InputStream in = new FileInputStream(f)) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[8192];
            int n;
            while ((n = in.read(buf)) != -1) out.write(buf, 0, n);
            return new String(out.toByteArray(), "UTF-8");
        }
    }

    @PluginMethod
    public void list(PluginCall call) {
        JSObject ret = new JSObject();
        JSArray found = new JSArray();

        File books = booksDir();
        ret.put("dir", books == null ? "" : books.getAbsolutePath());

        if (books != null && books.isDirectory()) {
            File[] kids = books.listFiles();
            if (kids != null) {
                // Sorted, so the shelf does not reorder itself between
                // launches on whatever order the filesystem felt like.
                Arrays.sort(kids);
                for (File dir : kids) {
                    if (!dir.isDirectory()) continue;
                    File manifest = new File(dir, "book.json");
                    if (!manifest.isFile()) continue;
                    try {
                        JSObject entry = new JSObject();
                        entry.put("dir", dir.getName());
                        entry.put("base", dir.getAbsolutePath());
                        entry.put("manifest", readText(manifest));
                        found.put(entry);
                    } catch (IOException e) {
                        // One unreadable book must not empty the shelf.
                    }
                }
            }
        }

        ret.put("books", found);
        call.resolve(ret);
    }
}
