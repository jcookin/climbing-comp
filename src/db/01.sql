-- Enable foreign keys for database on every session
PRAGMA foreign_keys = ON;

-------------------------------------------------
-- Users requiring unique names
-- Team assignment not required at user creation
-------------------------------------------------
CREATE TABLE IF NOT EXISTS climbers (
	climber_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
	team_id INTEGER DEFAULT -1,
  password_hash BLOB NOT NULL,
  is_admin INTEGER DEFAULT 0,
  common_name TEXT DEFAULT NULL,
  created_date DATETIME DEFAULT (datetime('now')),
  FOREIGN KEY (team_id)
    REFERENCES teams (team_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);

-------------------------------------------------------------
-- Route name and difficulty management
-- Grade values: v0 = 0, plus/minus not accounted for
-- Assumed no route names will be duplicated
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS routes (
  route_id INTEGER PRIMARY KEY AUTOINCREMENT,
  route_name TEXT NOT NULL UNIQUE,
  route_grade INTEGER NOT NULL,
  route_created DATETIME DEFAULT (datetime('now')),
  route_created_by TEXT DEFAULT NULL,
  route_points INTEGER NOT NULL
);

--------------
-- Team names
--------------
CREATE TABLE IF NOT EXISTS teams (
  team_id INTEGER PRIMARY KEY AUTOINCREMENT,
  team_name TEXT NOT NULL UNIQUE,
  created_date DATETIME DEFAULT (datetime('now'))
);

---------------------------------------------------
-- Maintains the relationship of routes to users
-- keeps count of the number of attempts and sends
---------------------------------------------------
CREATE TABLE IF NOT EXISTS attempts_sends (
  route_id INTEGER,
  climber_id INTEGER,
  attempt_num INTEGER default 0,
  is_sent INTEGER default 0,
  send_date DATETIME DEFAULT (datetime('now')),
  PRIMARY KEY (route_id, climber_id),
  FOREIGN KEY (route_id)
      REFERENCES routes (route_id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION,
  FOREIGN KEY (climber_id) 
      REFERENCES climbers (climber_id) 
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);

-----------------------------------------------
-- Miscellaneous data needed for app functions
-----------------------------------------------
CREATE TABLE IF NOT EXISTS app_data (
  register_code INTEGER NOT NULL
);

-- Add default registration code
INSERT INTO app_data (register_code) VALUES ('ouchmyfingies');
-- Add a default "null" team name for user defaults foreign key needs
INSERT INTO teams (team_id, team_name) VALUES (-1, "") ON CONFLICT DO NOTHING;