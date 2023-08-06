(do
  (import requests)
  (import [bs4 [BeautifulSoup]])
  (defn test []
    (download "http://loveread.ec/read_book.php?id=70351" True)
    )
  (defn download [book_url &optional [save True] [folder ""]]
    (setv base_url "http://loveread.ec/read_book.php?id=%(id)s&p=%(page)s")
    (setv ID (first (.split (get (.split book_url "id=") -1) "&")))
    (setv PAGES (do 
                  (setv r (.((. requests get) (% base_url {"id" ID "page" 1}))))
                  (setv r.encoding "Windows-1251")
                  (setv soup (BeautifulSoup  r.text "html.parser"))
                  (int (.get_text (get (.select soup ".navigation a") -2)))
                  ))
    (setv NAME (.get_text (first (.select soup ".tb_read_book h2 a"))))
    
    
    (setv book [])
    (for [i (range 1 (+ 1 PAGES))]
      (setv url (% base_url {"id" ID "page" i}))
      (print "downloading from " url)
      (setv r (.((. requests get) url)))
      (setv r.encoding "Windows-1251")
      (setv soup (BeautifulSoup  r.text "html.parser"))
      (setv main  (.select soup "p.MsoNormal"))
      (+= book [(+ (.get_text (first main)) "")])
      ;(for [elem main] (+= book [(+ (.get_text elem) "///")]))
      )
    (setv handler (open (+ folder NAME ".txt") "w+"))
    (setv strBook (.join "\r\n\r\n" book))
    (if save 
      (do
        (for [i (list strBook)]
          (try
            (.write handler i)
            (except [e ValueError] (.write handler "?"))
            
            )
          )
        )
      )
    (return strBook)
    )
  
  )