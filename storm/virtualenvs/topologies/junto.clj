(ns microbrew
  (:use     [streamparse.specs])
  (:gen-class))

(defn microbrew [options]
   [
    ;; spout configuration
    {"queue-spout" (python-spout-spec
          options
          "spouts.qspout.QSpout"
          {"incoming_data" ["message"]}
          )
    }
    ;; bolt configuration
    {"filter" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {["queue-spout" "incoming_data"] :shuffle}
	  ;; class to run
          "bolts.filter.Filter"
	  ;; output spec, what tuples does this bolt emit?
          {"filtered" ["message"]}
          ;;:p 2
          )
    }
    ;; bolt configuration
    {"sentiment-detection" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {"filter" :shuffle}
	   ;; class to run
          "bolts.sentiment.SentimentDetector"
	  ;; output spec, what tuples does this bolt emit?
          {"pro" ["rank" "message"]
	   "con" ["rank" "message"]}
          )
    }
    ;; bolt configuration
    {"db-load" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {["sentiment-detection" "pro"] :shuffle
	   ["sentiment-detection" "con"] :shuffle}
	   ;; class to run
          "bolts.db_handler.DBLoader"
	  ;; output spec, what tuples does this bolt emit?
	  []
          )
    }
    ;; bolt configuration
    {"reactor" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {["sentiment-detection" "pro"] :shuffle
	   ["sentiment-detection" "con"] :shuffle}
	   ;; class to run
          "bolts.reactors.Reactor"
	  ;; output spec, what tuples does this bolt emit?
          {"reaction" ["action" "message"]}
          )
    }
    ;; bolt configuration
    {"avatar-chooser" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {["reactor" "reaction"] :shuffle}
	   ;; class to run
          "bolts.chooser.AvatarChooser"
	  ;; output spec, what tuples does this bolt emit?
          {"assignment" ["avatar" "action" "message"]}
          )
    }
    ;; bolt configuration
    {"actor" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {["avatar-chooser" "assignment"] :shuffle}
	   ;; class to run
          "bolts.actor.ActorBolt"
	  ;; output spec, what tuples does this bolt emit?
          []
          )
    }
  ]
)
