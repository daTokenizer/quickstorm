(ns quickstorm
  (:use     [streamparse.specs])
  (:gen-class))

(defn quickstorm [options]
   [
    ;; spout configuration
    {"queue-spout" (python-spout-spec
          options
          "spouts.qspout.QSpout"
          ["message"]
          )
    }
    ;; bolt configuration
    {"actionbolt" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {"queue-spout" :shuffle
	   ["actionbolt" "next_action"] "action"}
	  ;; class to run
          "bolts.actionbolt.ActionBolt"
	  ;; output spec, what tuples does this bolt emit?
          {"next_action" ["action" "data"]
	  "output_to_queue" ["data"]}
          ;;:p 2
          )
    }
    ;; bolt configuration
    {"queue-bolt" (python-bolt-spec
          options
	  ;; inputs, where does this bolt recieve it's tuples from?
          {["actionbolt" "output_to_queue"] :shuffle}
	   ;; class to run
          "bolts.queuebolt.QBolt"
	  ;; output spec, what tuples does this bolt emit?
          []
          )
    }
  ]
)
