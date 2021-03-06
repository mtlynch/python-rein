��    /      �  C           r    `  �  )   �  
   	     "	  
   7	  
   B	  '   M	     u	     �	     �	     �	     �	     �	     �	  9   �	     &
     9
     U
     g
  U  �
     �     �     �               ,  
   :     E     ^     l  
   �     �     �     �     �     �     �     �          (     @     W     o     �     �    �  �  �  �  s  .        0     A     `     o  #        �     �  $   �     �     �       
   !  >   ,     k     q     �  &   �  �  �     }     �     �     �     �     �     �               ,     G     ^     q     �  	   �     �     �     �     �     �       $   ,     Q     m  	   ~                                 '                      (          .      
           #                 )           &              /       *          -          %   ,   $                         "              	       !   +                   
    Rein is a decentralized professional services market and Python-rein is a client
that provides a user interface. Use this program from your local browser or command 
line to create an account, post a job, bid, etc.


    Quick start:
        $ rein start     - create an identity, run the Web UI
        $ rein buy       - request microhosting
        $ rein sync      - push your identity to microhosting servers
        $ rein status    - get user status, or dump of job's documents


    Workers
        $ rein bid       - view and bid on jobs
        $ rein deliver   - complete job by providing deliverables


    Disputes
        $ rein workerdispute    - worker files dispute
        $ rein creatordispute   - job creator files dispute
        $ rein resolve          - mediator posts decision

    For more info and the setup guide visit: http://reinproject.org
     
    Setup or import an identity.

    You will choose a name or handle for your account, include public contact information, 
    and a delegate Bitcoin address/private key that the program will use to sign documents
    on your behalf. An enrollment document will be created and you will need to sign it
    with your master Bitcoin private key.
     1 - Create new account
2 - Import backup
 Bid amount Choose Job to bid on Choose bid Choose job Choose job associated with deliverables Choose mediator Delegate Bitcoin address Delegate Bitcoin private Key Deliverables Description Dispute detail Disputes Do you want to import a backup or create a new account?

 Email / Bitmessage Error connecting to server. Expiration (days) File containing signed document Funds for each job in Rein are stored in two multisig addresses. One address
is for the primary payment that will go to the worker on completion. The
second address pays the mediator to be available to resolve a dispute
if necessary. The second address should be funded according to the percentage
specified by the mediator and is in addition to the primary payment. The
listing below shows available mediators and the fee they charge. You should
consider the fee as well as any reputational data you are able to find when
choosing a mediator. Your choice may affect the number and quality of bids Invalid address Invalid signature Job name Master Bitcoin address Mediator Fee Name / Handle None found Not a valid private key. Please enter  Register as a mediator? Resolution Signed enrollment Signed mediator payment Signed primary payment Tags Verifying block times... Welcome to Rein. bid submitted complete, dispute resolved complete, work accepted deliverables submitted disputed by job creator disputed by worker job awarded posted Project-Id-Version: 0.2
POT-Creation-Date: 2016-12-21 11:00+PST
PO-Revision-Date: 2016-12-21 11:00+PST
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
 
    Rein es un mercado profesional, descentralizado, de servicios y Python-rein es el cliente
que provee la interfaz de usuario. Usa este programa desde tu navegador o línea de comandos 
para crear una cuenta, publicar un trabajo, ofertarse para un trabajo, etc.


    Iniciándose:
        $ rein start     - crea una identidad, ejecuta la interfaz de usuario web
        $ rein buy       - pide microhosting
        $ rein sync      - sincroniza tu identidad con los servidores
        $ rein status    - comprobar estado de identidad, transacción, etc


    Trabajadores
        $ rein bid       - mirar y ofertarse para un trabajo
        $ rein deliver   - completar trabajo suministrando entregas


    Disputas
        $ rein workerdispute    - mediante este comando el trabajador puede comenzar un conflicto,
								   debe especificar la razón de la misma, i.e. el epmpleador no 
								   fue razonable, etc, enlazar pruebas 
        $ rein creatordispute   - mediante este comando el empleador puede comenzar un conflicto, 
								   debe especificar la razón de la misma, i.e. el trabajador no realizó 
								   la entrega o hizo un mal trabajo, etc
        $ rein resolve          - este comando es el usado por el mediador para revisar la información 
								   dada por el empleador y el trabajador con el fin de decidir cómo 
 								   resolver el conflicto.

    Para más información y guía de configuración visitar: http://reinproject.org
     
    Configurar o importar una identidad.

    Escoger un nombre de usuario para la cuenta, incluyendo información pública de contacto, 
    y una dirección/llave privada delegada de Bitcoinand que el programa utilizará para firmar documentos
    a tu favor. Se creará un documento llamado matrícula el cual deberás firmar con 
    la llave privada de la dirección Bitcoin principal .
     1 - Crear nueva cuenta
2 - Restaurar respaldo
 Ofrecer cantidad Escoger trabajo para ofrecerse Escoger oferta Escoger trabajo Escoger trabajo asociado a entregas Escoger mediador Dirección Bitcoin delegada Llave privada de dirección delegada Entregas Descripción Detalles de conflicto Conflictos Deseas restaurar copia de respaldo o crear una nueva cuenta?

 Email Error conectándose al servidor Expira (días) Archivo que contiene documento firmado Los fondos para cada trabajo en Rein se almacenan en dos direcciones multi-firma. 
En la primera se transfieren los pagos al trabajador, tras terminar el trabajo,
en la segunda dirección, los pagos al mediador que resolverá los conflictos.
A la segunda dirección se le transferirá un monto de acuerdo a los honorarios establecidos
por el mediador, en adición a los fondos transferidos a la primera dirección. La lista mostrada
debajo muestra los mediadores disponibles y sus respectivos honorarios. Debes considerar
dichos honorarios así como los datos disponibles de reputación al buscar un mediador.
La elección de un mediador podría influir en el número y calidad de las ofertas. Dirección no válida Firma no válida Nombre del trabajo Dirección Bitcoin principal Honorarios del mediador Nombre No se encontró Llave privada no válida Por favor entre Registrarse como mediador? Decisión del mediador Matrícula firmada Pago de mediador firmado Pago principal firmado Etiquetas Verificando block ... Bienvenido a Rein oferta enviada completo, conflicto resuelto completo, trabajo aceptado entregas enviadas dispudato por el creador del trabajo dispudato por el trabajador trabajo otorgado publicado 