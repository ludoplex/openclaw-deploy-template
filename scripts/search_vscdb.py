"""Search Cursor vscdb files for ggLeap, Odyssey, Pearson VUE content."""
import sqlite3
import os
import json

db_paths = [
    r"C:\Users\user\.cursor\worktrees\Cursor_working_directory_misc\aat\cursor_session_export\state.vscdb",
]

search_terms = ['ggleap', 'ggcircuit', 'odyssey', 'withodyssey', 'pearson', 'pearsonvue', 'igames', 'steamcafe', 'esa']

for db_path in db_paths:
    print(f"\n=== Searching: {os.path.basename(os.path.dirname(db_path))} ===")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        # Search ItemTable for chat content
        if 'ItemTable' in tables:
            cursor.execute("SELECT key, value FROM ItemTable LIMIT 5")
            for key, value in cursor.fetchall():
                print(f"Key: {key[:80]}...")
                
            # Search for our terms
            for term in search_terms:
                cursor.execute(f"SELECT key, value FROM ItemTable WHERE value LIKE ?", (f'%{term}%',))
                results = cursor.fetchall()
                if results:
                    print(f"\n--- Found '{term}': {len(results)} results ---")
                    for key, value in results[:3]:
                        print(f"Key: {key[:50]}")
                        # Try to pretty print if JSON
                        try:
                            if value and len(value) > 100:
                                print(f"Value preview: {value[:500]}...")
                            else:
                                print(f"Value: {value}")
                        except:
                            print(f"Value: {str(value)[:200]}...")
                        print()
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

print("\nDone.")
