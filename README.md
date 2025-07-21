# 🎛️ AutomatePro: Basit ve Güçlü GUI Tabanlı Makro Kaydedici

AutomatePro, fare tıklamalarınızı ve klavye eylemlerinizi kolayca kaydedip tekrar oynatmanızı sağlayan, Python ve PyQt6 ile oluşturulmuş hafif ve sezgisel bir masaüstü uygulamasıdır. İster tekrarlayan görevleri otomatikleştirin, ister hızlı iş akışları oluşturun, AutomatePro masaüstü otomasyonu için başvuracağınız araçtır.

Gerçek zamanlı geri bildirim, temiz arayüz, modern temalar, eylemleri düzenleme ve kaydetme/yükleme desteği ile AutomatePro hem güçlü hem de başlangıç seviyesi kullanıcılar için dostudur.

## 🚀 Özellikler

  * **🎥 Kayıt & Oynatma**: Klavye ve fare eylemlerinizi kaydedin ve hassas zamanlamayla tekrar oynatın.
  * **✏️ Eylemleri Düzenle & Sil**: Kaydettikten sonra bir eylemi beğenmediniz mi? Sağ tıklayarak **gecikmesini, tuşunu veya fare koordinatlarını** değiştirin ya da tamamen silin.
  * **⏱️ Akıllı Gecikme Kaydı**: Eylemler arasındaki bekleme süresini **otomatik olarak** hesaplar ve kaydeder, böylece makrolarınız daha doğal çalışır.
  * **🔦 Canlı Oynatma Vurgusu**: Makro çalışırken, o an yürütülen eylem listede **vurgulanarak** akışı kolayca takip etmenizi sağlar.
  * **🔁 Tekrarlı Otomasyon**: Makronuzun kaç kez otomatik olarak tekrarlanacağını modern +/- butonları ile kolayca ayarlayın.
  * **💾 Makroları Kaydet & Yükle**: Kaydettiğiniz eylemleri `.json` dosyalarına aktarın ve istediğiniz zaman yeniden yükleyin.
  * **🧾 Gelişmiş Eylem Listesi**: Eylemleriniz, gecikme süreleriyle birlikte anında listede belirir.
  * **🎨 Modern Temalar**: Tek bir tıklamayla modern ve şık bir **karanlık mod** ile temiz bir **aydınlık mod** arasında geçiş yapın.
  * **📣 Durum Çubuğu Bildirimleri**: “Kaydediliyor...”, “Oynatılıyor...” veya “Hazır” gibi net durum mesajları alın.
  * **🧵 Güvenli ve Kesintili Oynatma**: Oynatma, uygulamanın donmasını önlemek için ayrı bir iş parçacığında (thread) çalışır. Oynatmayı istediğiniz zaman güvenle durdurabilirsiniz.

-----

## 📚 Nasıl Kullanılır?

**1. Bağımlılıkları Yükleyin**

Python 3'ün kurulu olduğundan emin olun. Ardından gerekli paketleri yükleyin:

```bash
pip install PyQt6 pynput
```

**2. Makronuzu Kaydedin**

  * "Record" (Kaydet) butonuna tıklayın.
  * Fare tıklamalarınızı ve tuş vuruşlarınızı gerçekleştirin.
  * Bitirdiğinizde "Stop" (Durdur) butonuna tıklayın.

Eylemleriniz, "Recorded Actions" (Kaydedilen Eylemler) listesinde görünecektir.

**3. Makroyu Düzenleyin (İsteğe Bağlı)**

  * Listeden bir eylemi değiştirmek veya silmek için üzerine **sağ tıklayın**.
  * Açılan menüden "Edit" (Düzenle) veya "Delete" (Sil) seçeneğini kullanın.

**4. Makroyu Oynatın**

  * "Repeats" (Tekrar) kontrolünü kullanarak tekrar sayısını ayarlayın.
  * "Play" (Oynat) butonuna tıklayarak oynatmayı başlatın.
  * İstediğiniz zaman iptal etmek için "Stop Playback" (Oynatmayı Durdur) butonunu kullanın.

**5. Makroları Kaydedin veya Yükleyin**

  * "Save" (Kaydet) butonuna tıklayarak eylemlerinizi bir `.json` dosyasına aktarın.
  * "Load" (Yükle) butonuna tıklayarak daha önce kaydettiğiniz bir makroyu açın.

-----

## 🛠 Kullanılan Teknolojiler

  * **Python 3**
  * **PyQt6** – Kullanıcı arayüzünü oluşturmak için
  * **Pynput** – Klavye/fare girdilerini yakalamak ve simüle etmek için

-----

## 💡 İdeal Kullanım Alanları

  * Tekrarlayan veri girişlerini otomatikleştirmek
  * Çok adımlı iş akışlarını çalıştırmak
  * Kaydedilmiş iş akışlarını mükemmelleştirmek ve ince ayar yapmak
  * Hızlı kullanıcı arayüzü demoları veya testleri oluşturmak
  * Rutin masaüstü görevlerinde zaman kazanmak
