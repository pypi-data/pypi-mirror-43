(do
  
  (defn bar [] (print "bar"))
  (defn s-lambda [mode action arr]
    (list (mode (fn [x] (if (in (type x) [list set arr]) (supermap action x) (action x))) arr))
    )
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
  (defn execute [code &optional [mode "char"][input ""]]
    (.execute (BrainFuckMachine) code mode input))
  
  
  (defclass BFM [object]
    
    (defn --init-- [self]
      (setv self.output []
            self.input [0]
            self.code []
            self.pointer 0
            self.memory [0]
            self.DICT_allowed ["+" "-" "<" ">" "." "," "[" "]"]
            self.DICT_convert ["+" "-" "<" ">" "." ","]
            
            )
      )
    (defn --str-- [self]
      (str {
      "input" self.input
      "output" self.output
      "memory" self.memory
      "code" self.code
      })
      )
    (defmacro cell []
      `(get self.memory self.pointer))
    (defn translate [self code]
      (if (= (type code) str) 
        (do
          (for [[k v] (enumerate self.DICT_convert)] (setv code (.replace code v (str k))))
          (print code)
          
          
          (eval (read-str (+ "[" (.join " " code) "]")))
          )
        code
        )
      
      
      )
    (defn execute [self code &optional [input []][is_fn False][mode "int"]]
      (if (not is_fn)(do
                       (setv code (self.translate code))
                       (setv self.code code)
                       (if (= str (type input)) (setv input (s-lambda map ord input)))
                       (setv self.input input)
                       ))
      
      
      
      (for [c code]
        (cond 
          [(= c 0) (+= (cell) 1)]
          [(= c 1) (-= (cell) 1)]
          [(= c 2) (do (+= self.pointer 1) (if (< (len self.memory) self.pointer)))]
          [(= c 3) (do (-= self.pointer 1) (if (> 0 self.pointer) (do (setv self.pointer 0)(.insert self.memory 0 0))))]
          [(= c 4) (.append self.output (cell))]
          [(= c 5) (setv (cell) (if self.input (.pop self.input 0) 0))]
          [(in (type c) [list set tuple]) (unless (= 0 (cell)) (self.execute c input True))]
          )
        
        )
      (if is_fn
        (if (!= 0 (cell)) (self.execute code input True))
        )
      (if (= mode "char")
        (setv self.output (s-lambda map chr self.output))
        )
      (return self.output)
      )
    )
  )
(setv b (BFM))
(print (b.execute ",>,< [ > [ >+ >+ << -] >> [- << + >>] <<< -] >>." :mode "int" :input [14 88]))
(print b)