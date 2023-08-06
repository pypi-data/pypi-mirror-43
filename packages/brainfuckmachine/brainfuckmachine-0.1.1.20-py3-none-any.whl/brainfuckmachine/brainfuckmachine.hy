(do

(defn bar [] (print "bar"))

(defclass BrainFuckMachine [object]
  (defn --init-- [self]
    (setv
    self.state [0]
   self.pointer 0
   self.cursor 0
   self.input ""
   self.focus 0
   self.shift 0
   self.output ""
   self.bookmarks {}
   self.skip None
         ))
  
  (defn operate[self s &optional [log False]]
    (if (= "[" s) (+= self.shift 1))
    (cond
      [(= "[" s) (do (assoc self.bookmarks self.shift self.focus) 
                     (if (= 0 (get self.state self.pointer)) (setv self.skip self.shift)) )]
      [(= "]" s) (do (if (= self.skip self.shift) (setv self.skip None))
                     (if (!= (get self.state self.pointer) 0)
                       (setv self.focus (- (get self.bookmarks self.shift) 1))))]
      [(!= None self.skip) (return False)]
      [(= "+" s) (+= (. self state [self.pointer]) 1)]
      [(= "-" s) (-= (. self state [self.pointer]) 1)]
      [(= "." s) (+= self.output (chr (get self.state self.pointer)))]
      [(= "," s) (do (assoc self.state self.pointer
                            (ord (get self.input self.cursor)))
                     (+= self.cursor 1))]
      [(= ">" s) (do (+= self.pointer 1)
                     (if (>= self.pointer (len self.state))
                       (.append self.state 0)))]
      [(= "<" s) (do (-= self.pointer 1)
                     (if (< self.pointer 0)
                       (do (.insert self.state 0 0)
                           (setv self.pointer 0))))]
      )
    (if (= "]" s) (-= self.shift 1))
    (if log (self.log))
    )
  
  (defn log [self]
    (print {
            "focus" self.focus
            "pointer" self.pointer
            "state" self.state
            "shift" self.shift
            "output" self.output
            "skip" self.skip
            "bookmarks" self.bookmarks
            }))
  (defn execute [self code &optional [mode "char"][input ""]]
    (setv self.focus 0)
    (if input
      (setv self.input
            (list(map (fn [cell]
                        (if (isinstance cell str)
                          cell
                          (chr cell)
                          )
                        ) input)
                  )
            )
      )
    (print self.input)
    (while (< self.focus (len code))
      (self.operate (get code self.focus))
      (+= self.focus 1)
      )
    
    (cond
      [(= mode "char") (return self.output)]
      [(= mode "int") (return (list(map (fn[cell] (ord cell)) self.output)))])
    )
  )
(defn execute [code]
  (.execute (BrainFuckMachine) code))

  )
