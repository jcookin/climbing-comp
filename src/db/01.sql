-------------------------------------------------
-- Users requiring unique names
-- Team assignment not required at user creation
-------------------------------------------------
CREATE TABLE IF NOT EXISTS climbers (
	climber_id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
	team_id INTEGER DEFAULT 0,
  user_pass TEXT NOT NULL,
  is_admin INTEGER DEFAULT 0,
  created_date DATETIME DEFAULT (datetime('now')),
  FOREIGN KEY (team_id)
    REFERENCES teams (team_id)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
  
) WITHOUT ROWID;

-------------------------------------------------------------
-- Route name and difficulty management
-- Grade values: v0 = 0, -0 = v0-, 0.5 = v0+, if +/- is used
-- Assumed no route names will be duplicated
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS routes (
  route_id INTEGER PRIMARY KEY,
  route_name TEXT NOT NULL UNIQUE,
  route_grade INTEGER NOT NULL,
  route_created DATETIME DEFAULT (datetime('now'))
) WITHOUT ROWID;

--------------
-- Team names
--------------
CREATE TABLE IF NOT EXISTS teams (
  team_id INTEGER PRIMARY KEY,
  team_name TEXT NOT NULL UNIQUE,
  created_date DATETIME DEFAULT (datetime('now'))
) WITHOUT ROWID;

---------------------------------------------------
-- Maintains the relationship of routes to users
-- keeps count of the number of attempts and sends
---------------------------------------------------
CREATE TABLE IF NOT EXISTS attempts_sends (
  route_id INTEGER,
  climber_id INTEGER,
  attempt_num INTEGER default 0,
  send_num INTEGER default 0,
  send_date DATETIME DEFAULT (datetime('now'))
  PRIMARY KEY (route_id, climber_id),
  FOREIGN KEY (route_id) 
      REFERENCES routes (route_id) 
         ON DELETE CASCADE
         ON UPDATE NO ACTION,
  FOREIGN KEY (climber_id) 
      REFERENCES climbers (climber_id) 
         ON DELETE CASCADE
         ON UPDATE NO ACTION
) WITHOUT ROWID;

-----------------------------------------------
-- Miscellaneous data needed for app functions
-----------------------------------------------
CREATE TABLE IF NOT EXISTS app_data (
  -- Generate random share code for user creation
  register_code INTEGER DEFAULT (lower(hex(randomblob(16)))),
  pass_hash TEXT DEFAULT (randomblob(32)),
) WITHOUT ROWID;
