---
title: "تطوير التطبيقات"
description: "لماذا كتابة تطبيقات مخصصة لـ I2P، المفاهيم الأساسية، خيارات التطوير، ودليل البدء"
slug: "applications"
aliases:
  - "/ar/docs/develop/applications"
  - "/ar/docs/develop/applications/"
  - "/ar/applications"
  - "/ar/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## لماذا كتابة كود خاص بـ I2P؟

هناك طرق متعددة لاستخدام التطبيقات في I2P. باستخدام [I2PTunnel](/docs/api/i2ptunnel/)، يمكنك استخدام التطبيقات العادية دون الحاجة لبرمجة دعم صريح لـ I2P. هذا فعال جداً لسيناريوهات العميل-الخادم، حيث تحتاج للاتصال بموقع ويب واحد. يمكنك ببساطة إنشاء tunnel باستخدام I2PTunnel للاتصال بذلك الموقع، كما هو موضح في الشكل 1.

إذا كان تطبيقك موزعاً، فسيتطلب اتصالات بعدد كبير من النظراء. باستخدام I2PTunnel، ستحتاج إلى إنشاء tunnel جديد لكل نظير تريد الاتصال به، كما هو موضح في الشكل 2. يمكن بالطبع أتمتة هذه العملية، لكن تشغيل العديد من instances الخاصة بـ I2PTunnel ينشئ قدراً كبيراً من الأعباء الإضافية. بالإضافة إلى ذلك، مع العديد من البروتوكولات ستحتاج إلى إجبار الجميع على استخدام نفس مجموعة المنافذ لجميع النظراء — على سبيل المثال إذا كنت تريد تشغيل دردشة DCC بشكل موثوق، يحتاج الجميع إلى الاتفاق على أن المنفذ 10001 هو لـ Alice، والمنفذ 10002 هو لـ Bob، والمنفذ 10003 هو لـ Charlie، وهكذا، حيث أن البروتوكول يتضمن معلومات محددة لـ TCP/IP (المضيف والمنفذ).

تطبيقات الشبكة العامة غالباً ما ترسل كمية كبيرة من البيانات الإضافية التي يمكن استخدامها لتحديد هوية المستخدمين. أسماء المضيفين وأرقام المنافذ والمناطق الزمنية ومجموعات الأحرف وغيرها غالباً ما يتم إرسالها دون إعلام المستخدم. وبالتالي، فإن تصميم بروتوكول الشبكة خصيصاً مع وضع إخفاء الهوية في الاعتبار يمكن أن يتجنب تعريض هويات المستخدمين للخطر.

هناك أيضاً اعتبارات كفاءة يجب مراجعتها عند تحديد كيفية التفاعل على I2P. مكتبة streaming والأشياء المبنية عليها تعمل بمصافحات مشابهة لـ TCP، بينما بروتوكولات I2P الأساسية (I2NP وI2CP) مبنية بشكل صارم على الرسائل (مثل UDP أو في بعض الحالات IP الخام). التمييز المهم هو أنه مع I2P، الاتصال يعمل عبر شبكة طويلة وسمينة — كل رسالة من طرف إلى طرف ستكون لها زمن استجابة غير قليل، لكن قد تحتوي على حمولات تصل إلى عدة كيلوبايت. التطبيق الذي يحتاج طلب واستجابة بسيطين يمكنه التخلص من أي حالة وإسقاط زمن الاستجابة المتكبد بواسطة مصافحات البدء والإنهاء باستخدام datagram (بأفضل جهد) دون الحاجة للقلق حول اكتشاف MTU أو تجزئة الرسائل.

![إنشاء اتصال خادم-عميل باستخدام I2PTunnel يتطلب فقط إنشاء tunnel واحد.](/images/i2ptunnel_serverclient.png)

*الشكل 1: إنشاء اتصال خادم-عميل باستخدام I2PTunnel يتطلب فقط إنشاء tunnel واحد.*

![إعداد الاتصالات لتطبيقات الند للند يتطلب عدداً كبيراً جداً من الأنفاق.](/images/i2ptunnel_peertopeer.png)

*الشكل 2: إعداد الاتصالات لتطبيقات الند للند يتطلب عدداً كبيراً جداً من الأنفاق.*

باختصار، عدد من الأسباب لكتابة كود خاص بـ I2P:

- إنشاء عدد كبير من مثيلات I2PTunnel يستهلك كمية غير تافهة من الموارد، مما يشكل مشكلة للتطبيقات الموزعة (نفق جديد مطلوب لكل نظير).
- بروتوكولات الشبكة العامة غالباً ما ترسل الكثير من البيانات الإضافية التي يمكن استخدامها لتحديد هوية المستخدمين. البرمجة خصيصاً لـ I2P تتيح إنشاء بروتوكول شبكة لا يسرب مثل هذه المعلومات، مما يحافظ على إخفاء هوية المستخدمين وأمانهم.
- بروتوكولات الشبكة المصممة للاستخدام على الإنترنت العادي يمكن أن تكون غير فعالة على I2P، وهي شبكة ذات زمن استجابة أعلى بكثير.

يدعم I2P واجهة [plugins معيارية](/docs/specs/plugin/) للمطورين بحيث يمكن دمج التطبيقات وتوزيعها بسهولة.

التطبيقات المكتوبة بلغة Java والقابلة للوصول/التشغيل باستخدام واجهة HTML عبر webapps/app.war القياسية قد يتم النظر في إدراجها ضمن توزيعة I2P.

---

## المفاهيم المهمة

هناك بعض التغييرات التي تتطلب التكيف معها عند استخدام I2P:

### Destination ~= host+port

يقوم التطبيق الذي يعمل على I2P بإرسال الرسائل من وإستقبالها إلى نقطة نهاية آمنة تشفيرياً وفريدة — "destination" (وجهة). من ناحية بروتوكولي TCP أو UDP، يمكن اعتبار الـ destination (إلى حد كبير) مكافئة لزوج اسم المضيف ورقم المنفذ، رغم وجود بعض الاختلافات.

- I2P destination نفسه هو بناء تشفيري — جميع البيانات المرسلة إليه مشفرة كما لو كان هناك نشر شامل لـ IPsec مع موقع النقطة النهائية المجهول الهوية موقّع كما لو كان هناك نشر شامل لـ DNSSEC.
- I2P destinations هي معرفات متنقلة — يمكن نقلها من I2P router إلى آخر (أو يمكن حتى "تعدد المنازل" — العمل على عدة routers في آن واحد). هذا مختلف تماماً عن عالم TCP أو UDP حيث يجب أن تبقى نقطة نهاية واحدة (منفذ) على مضيف واحد.
- I2P destinations قبيحة وكبيرة — خلف الكواليس، تحتوي على مفتاح عام ElGamal بحجم 2048 بت للتشفير، ومفتاح عام DSA بحجم 1024 بت للتوقيع، وشهادة بحجم متغير، والتي قد تحتوي على إثبات عمل أو بيانات مُعماة.

توجد طرق حالية للإشارة إلى هذه الوجهات الكبيرة والقبيحة بأسماء قصيرة وجميلة (مثل "irc.duck.i2p")، لكن هذه التقنيات لا تضمن التفرد العالمي (لأنها مخزنة محلياً في قاعدة بيانات على جهاز كل شخص) والآلية الحالية ليست قابلة للتوسع أو آمنة بشكل خاص (يتم إدارة التحديثات لقائمة المضيفين باستخدام "اشتراكات" في خدمات التسمية). قد يكون هناك نظام تسمية آمن وقابل للقراءة البشرية وقابل للتوسع وفريد عالمياً في يوم من الأيام، لكن التطبيقات لا يجب أن تعتمد على وجوده، حيث أن هناك من لا يعتقد أن مثل هذا الوحش ممكن. [معلومات إضافية حول نظام التسمية](/docs/overview/naming/) متاحة.

بينما معظم التطبيقات لا تحتاج إلى التمييز بين البروتوكولات والمنافذ، فإن I2P *يدعم* ذلك. قد تحدد التطبيقات المعقدة بروتوكولاً ومنفذاً مصدرياً ومنفذاً وجهة، على أساس كل رسالة، لتعدد حركة البيانات على وجهة واحدة. راجع [صفحة datagram](/docs/api/datagrams/) للتفاصيل. تعمل التطبيقات البسيطة عن طريق الاستماع لـ "جميع البروتوكولات" على "جميع المنافذ" لوجهة معينة.

### إخفاء الهوية والسرية

يوفر I2P تشفيرًا شاملاً من طرف إلى طرف ومصادقة شفافة لجميع البيانات المنقولة عبر الشبكة — إذا أرسل Bob إلى وجهة Alice، فإن وجهة Alice فقط هي التي يمكنها استقبالها، وإذا كان Bob يستخدم مكتبة الرسائل المجزأة أو التدفق، فإن Alice تعلم بيقين أن وجهة Bob هي التي أرسلت البيانات.

بالطبع، يقوم I2P بإخفاء هوية البيانات المرسلة بين أليس وبوب بشكل شفاف، ولكنه لا يفعل شيئاً لإخفاء هوية محتوى ما يرسلونه. على سبيل المثال، إذا أرسلت أليس إلى بوب نموذجاً يحتوي على اسمها الكامل ووثائق الهوية الحكومية وأرقام بطاقاتها الائتمانية، فلا يمكن لـ I2P أن يفعل شيئاً حيال ذلك. وعلى هذا النحو، يجب على البروتوكولات والتطبيقات أن تضع في اعتبارها المعلومات التي تحاول حمايتها والمعلومات التي ترغب في الكشف عنها.

### يمكن أن تصل رسائل I2P البيانية إلى عدة كيلوبايت

يمكن اعتبار التطبيقات التي تستخدم datagrams الخاصة بـ I2P (سواء الخام أو القابلة للرد) بشكل أساسي من ناحية UDP — حيث أن datagrams غير مرتبة، وبأفضل جهد، وبدون اتصال — ولكن على عكس UDP، لا تحتاج التطبيقات للقلق حول اكتشاف MTU ويمكنها ببساطة إطلاق datagrams كبيرة. بينما الحد الأقصى اسمياً هو 32 كيلوبايت، يتم تجزئة الرسالة للنقل، مما يقلل من موثوقية الكل. datagrams التي تزيد عن حوالي 10 كيلوبايت غير موصى بها حالياً. راجع [صفحة datagram](/docs/api/datagrams/) للتفاصيل. بالنسبة للعديد من التطبيقات، 10 كيلوبايت من البيانات كافية لطلب أو استجابة كاملة، مما يسمح لها بالعمل بشفافية في I2P كتطبيق شبيه بـ UDP دون الحاجة لكتابة التجزئة، وإعادة الإرسال، إلخ.

---

## خيارات التطوير

هناك عدة وسائل لإرسال البيانات عبر I2P، لكل منها مزاياها وعيوبها. مكتبة streaming lib هي الواجهة الموصى بها، والتي تستخدمها غالبية تطبيقات I2P.

### مكتبة البث

إن [مكتبة البث الكاملة](/docs/api/streaming/) هي الآن الواجهة المعيارية. تسمح بالبرمجة باستخدام مقابس شبيهة بـ TCP، كما هو موضح في [دليل تطوير البث](#developing-with-the-streaming-library).

### BOB

BOB هو [Basic Open Bridge](/docs/legacy/bob/)، والذي يسمح لتطبيق بأي لغة برمجة بإنشاء اتصالات تدفق من وإلى I2P. في الوقت الحالي، يفتقر إلى دعم UDP، ولكن دعم UDP مخطط له في المستقبل القريب. يحتوي BOB أيضاً على عدة أدوات، مثل توليد مفاتيح الوجهة، والتحقق من أن العنوان يتوافق مع مواصفات I2P. يمكن العثور على المعلومات المحدثة والتطبيقات التي تستخدم BOB في هذا [موقع I2P](http://bob.i2p/).

### SAM، SAM V2، SAM V3

*SAM غير مُوصى به. SAM V2 مقبول، SAM V3 مُوصى به.*

SAM هو بروتوكول [Simple Anonymous Messaging](/docs/legacy/sam/) (الرسائل المجهولة البسيطة)، والذي يسمح لتطبيق مكتوب بأي لغة بالتواصل مع جسر SAM عبر مأخذ TCP عادي وجعل ذلك الجسر يتعامل مع كافة حركة مرور I2P الخاصة به، منسقاً بشفافية التشفير/فك التشفير والتعامل المبني على الأحداث. SAM يدعم ثلاثة أنماط تشغيل:

- التدفقات، عندما تريد أليس وبوب إرسال البيانات لبعضهما البعض بشكل موثوق ومرتب
- الرسائل القابلة للرد، عندما تريد أليس إرسال رسالة لبوب يمكن لبوب الرد عليها
- الرسائل الخام، عندما تريد أليس الحصول على أقصى عرض نطاق وأداء ممكن، وبوب لا يهتم بما إذا كان مرسل البيانات موثقاً أم لا (مثل البيانات المنقولة التي تحتوي على مصادقة ذاتية)

يهدف SAMv3 إلى نفس الهدف الذي يهدف إليه SAM و SAM V2، لكنه لا يتطلب تعدد الإرسال/إلغاء تعدد الإرسال. يتم التعامل مع كل I2P stream من خلال المقبس الخاص به بين التطبيق وجسر SAM. بالإضافة إلى ذلك، يمكن للتطبيق إرسال واستقبال البيانات المجمعة من خلال الاتصالات المجمعة مع جسر SAM.

[SAM V2](/docs/legacy/samv2/) هو إصدار جديد يُستخدم من قبل imule يعالج بعض المشاكل الموجودة في [SAM](/docs/legacy/sam/).

يتم استخدام [SAM V3](/docs/api/samv3/) من قبل imule منذ الإصدار 1.4.0.

### I2PTunnel

يتيح تطبيق I2PTunnel للتطبيقات بناء أنفاق محددة شبيهة بـ TCP للأقران من خلال إنشاء إما تطبيقات I2PTunnel 'عميل' (التي تستمع على منفذ محدد وتتصل بوجهة I2P محددة كلما تم فتح مقبس لذلك المنفذ) أو تطبيقات I2PTunnel 'خادم' (التي تستمع لوجهة I2P محددة وكلما تحصل على اتصال I2P جديد تقوم بعمل وكيل خارجي لمضيف/منفذ TCP محدد). هذه التدفقات نظيفة 8 بت، ومصادق عليها ومؤمنة من خلال نفس مكتبة streaming التي يستخدمها SAMv3، لكن هناك عبء غير بسيط مرتبط بإنشاء عدة نسخ I2PTunnel فريدة، حيث أن لكل منها وجهة I2P فريدة خاصة بها ومجموعة الأنفاق والمفاتيح الخاصة بها، إلخ.

### SOCKS

يدعم I2P بروكسي SOCKS V4 و V5. تعمل الاتصالات الصادرة بشكل جيد. قد تكون وظائف الاتصالات الواردة (الخادم) و UDP غير مكتملة وغير مختبرة.

### Ministreaming

*تم الحذف*

كانت هناك مكتبة "ministreaming" بسيطة في السابق، ولكن الآن ministreaming.jar يحتوي فقط على واجهات مكتبة streaming الكاملة.

### رسائل البيانات المجمعة

*موصى به لتطبيقات شبيهة بـ UDP*

تتيح [مكتبة Datagram](/docs/api/datagrams/) إرسال حزم شبيهة بـ UDP. من الممكن استخدام:

- الرسائل البيانية القابلة للرد
- الرسائل البيانية الخام

### I2CP

*غير مُوصى به*

[I2CP](/docs/specs/i2cp/) نفسه هو بروتوكول مستقل عن اللغة، ولكن لتنفيذ مكتبة I2CP في شيء آخر غير Java هناك كمية كبيرة من الكود يجب كتابتها (روتينات التشفير، تنظيم الكائنات، معالجة الرسائل غير المتزامنة، إلخ). بينما يمكن لشخص ما كتابة مكتبة I2CP في C أو شيء آخر، فمن المرجح أن يكون من الأكثر فائدة استخدام مكتبة SAM C بدلاً من ذلك.

### تطبيقات الويب

يأتي I2P مع خادم الويب Jetty، وتكوينه لاستخدام خادم Apache بدلاً من ذلك أمر مباشر. يجب أن تعمل أي تقنية تطبيقات ويب قياسية.

---

## ابدأ التطوير — دليل بسيط

التطوير باستخدام I2P يتطلب تثبيت I2P يعمل بشكل صحيح وبيئة تطوير من اختيارك. إذا كنت تستخدم Java، يمكنك بدء التطوير باستخدام [مكتبة streaming](#developing-with-the-streaming-library) أو مكتبة datagram. باستخدام لغة برمجة أخرى، يمكن استخدام SAM أو BOB.

### التطوير باستخدام مكتبة Streaming

يوضح المثال التالي كيفية إنشاء تطبيقات عميل وخادم شبيهة بـ TCP باستخدام مكتبة البث المتدفق.

سيتطلب هذا المكتبات التالية في مسار الفئات الخاص بك:

- `$I2P/lib/streaming.jar`: مكتبة streaming نفسها
- `$I2P/lib/mstreaming.jar`: المصنع والواجهات الخاصة بمكتبة streaming
- `$I2P/lib/i2p.jar`: فئات I2P القياسية وهياكل البيانات وواجهة برمجة التطبيقات والأدوات المساعدة

يمكنك الحصول على هذه من تثبيت I2P، أو إضافة التبعيات التالية من Maven Central:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

التواصل عبر الشبكة يتطلب استخدام مقابس الشبكة الخاصة بـ I2P. لتوضيح هذا، سننشئ تطبيقاً يمكن فيه للعميل إرسال رسائل نصية إلى الخادم، الذي سيطبع الرسائل ويرسلها مرة أخرى إلى العميل. بمعنى آخر، سيعمل الخادم كصدى.

سنبدأ بتهيئة تطبيق الخادم. هذا يتطلب الحصول على I2PSocketManager وإنشاء I2PServerSocket. لن نوفر للـ I2PSocketManagerFactory المفاتيح المحفوظة لـ Destination موجود، لذا سيقوم بإنشاء Destination جديد لنا. لذلك سنطلب من I2PSocketManager الحصول على I2PSession، حتى نتمكن من معرفة الـ Destination الذي تم إنشاؤه، حيث سنحتاج إلى نسخ ولصق هذه المعلومات لاحقاً حتى يتمكن العميل من الاتصال بنا.

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*مثال الكود 1: تهيئة تطبيق الخادم.*

بمجرد أن نحصل على I2PServerSocket، يمكننا إنشاء مثيلات I2PSocket لقبول الاتصالات من العملاء. في هذا المثال، سننشئ مثيل I2PSocket واحد، يمكنه التعامل مع عميل واحد فقط في كل مرة. سيتعين على الخادم الحقيقي أن يكون قادرًا على التعامل مع عملاء متعددين. للقيام بذلك، سيتعين إنشاء مثيلات I2PSocket متعددة، كل واحد منها في خيوط منفصلة. بمجرد أن ننشئ مثيل I2PSocket، نقرأ البيانات ونطبعها ونرسلها مرة أخرى إلى العميل.

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*مثال الكود 2: قبول الاتصالات من العملاء والتعامل مع الرسائل.*

عند تشغيل كود الخادم أعلاه، يجب أن يطبع شيئاً مثل هذا (ولكن بدون نهايات الأسطر، يجب أن يكون مجرد كتلة ضخمة واحدة من الأحرف):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
هذا هو التمثيل بتنسيق base64 لوجهة الخادم. سيحتاج العميل إلى هذا النص للوصول إلى الخادم.

الآن، سنقوم بإنشاء تطبيق العميل. مرة أخرى، هناك عدد من الخطوات المطلوبة للتهيئة. مرة أخرى، سنحتاج إلى البدء بالحصول على I2PSocketManager. لن نستخدم I2PSession و I2PServerSocket هذه المرة. بدلاً من ذلك، سنستخدم نص Destination الخاص بالخادم لبدء اتصالنا. سنطلب من المستخدم نص Destination، وننشئ I2PSocket باستخدام هذا النص. بمجرد أن نحصل على I2PSocket، يمكننا البدء في إرسال واستقبال البيانات من وإلى الخادم.

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*مثال الكود 3: بدء تشغيل العميل وربطه بتطبيق الخادم.*

أخيراً، يمكنك تشغيل كل من تطبيق الخادم وتطبيق العميل. أولاً، ابدأ تطبيق الخادم. سيطبع نص Destination (كما هو موضح أعلاه). بعد ذلك، ابدأ تطبيق العميل. عندما يطلب نص Destination، يمكنك إدخال النص الذي طبعه الخادم. سيقوم العميل بعدها بإرسال 'Hello I2P!' (مع سطر جديد) إلى الخادم، الذي سيطبع الرسالة ويرسلها مرة أخرى إلى العميل.

تهانينا، لقد نجحت في التواصل عبر I2P!

---

## التطبيقات الموجودة

اتصل بنا إذا كنت ترغب في المساهمة.

- [I2P-Bote](http://i2pbote.i2p/) - تواصل مع HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

انظر أيضًا جميع الإضافات في [plugins.i2p](http://plugins.i2p/)، والتطبيقات والكود المصدري المدرج في [echelon.i2p](http://echelon.i2p/)، وكود التطبيقات المستضاف في [git.repo.i2p](http://git.repo.i2p/).

انظر أيضاً التطبيقات المجمعة في توزيعة I2P - SusiMail و I2PSnark.

---

## أفكار التطبيقات

- خادم NNTP - كان هناك بعضها في الماضي، لا يوجد أي منها في الوقت الحالي
- خادم Jabber - كان هناك بعضها في الماضي، ويوجد واحد في الوقت الحالي، مع إمكانية الوصول إلى الإنترنت العام
- خادم مفاتيح PGP و/أو وكيل
- تطبيقات توزيع المحتوى / DHT - إحياء feedspace، نقل dijjer، البحث عن بدائل
- المساعدة في تطوير [Syndie](http://syndie.i2p2.de/)
- التطبيقات المعتمدة على الويب - السماء هي الحد الأقصى لاستضافة التطبيقات المعتمدة على خادم الويب مثل المدونات، pastebins، التخزين، التتبع، التغذيات، إلخ. أي تقنية ويب أو CGI مثل Perl أو PHP أو Python أو Ruby ستعمل.
- إحياء بعض التطبيقات القديمة، عدة منها كانت سابقاً في حزمة مصدر i2p - bogobot، pants، proxyscript، q، stasher، socks proxy، i2ping، feedspace
