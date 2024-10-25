# Bekk Shader Workshop
En workshop om shaderprogrammering

# Del 0: Intro til Shaders
[Link til GLSL.app](https://glsl.app/)

GLSL.app er en nettside som lar deg shaders i en web editor. Det er her vi skal løse oppgavene til workshopen.

Nettsiden vil lagre shadersene dine i cache, men lar deg laste den ned som en .glsl fil

Opprett en ny shader ved å trykke på **New** oppe til venstre på nettsiden.

Viewporten vil er moveable og resizable

`main()` funksjonen er vår main funksjon som kalles automatisk hver frame.

`uv` er en vektor som er posisjonen til pixelen vi skal beregne fargen til. Dens størrelse er basert på pikselens posisjon i forhold til viewport, oog går fra 0-1. Det vil si at hvis uv er (0.5,0.5), da er vi i sentrum av skjermen. 
> Origo (0,0) er nede til venstre


`out_color` er en innebygget `vec4` variabel som fungere i praksis som hele koden vår sin output. Denne representerer sluttfargen til fragmenten/pixelen vår.

# Del 1: Farger
## Oppgave 1.1: Farge 🎨
Prøv å sette hele skjermen til å være en farge. Du kan sette den til rød, eller gjøre om din favoritt hex kode (f.eks. `#253d31`) over til vec3 ved hjelp av [denne siden](https://airtightinteractive.com/util/hex-to-glsl/)


### Løsningsforslag
<details>
<summary>Se Løsningsforslag</summary>

```glsl
void main(){
    vec2 st = (2. * uv - 1.) * vec2(u_resolution.x / u_resolution.y, 1.);

    vec2 mouse = u_mouse.xy / u_resolution;
    vec3 red = vec3(1,0,0);
    out_color = vec4(
        red,
        1.
    );
}
```
</details>

## Oppgave 1.2: Gradient 
Nå er du blitt proff på å farge skjermen! 💪
Men nå skal du lage en gradient på skjermen.

> Hvordan gjør man dette? Bruk UV vektoren! 🗣️🗣️🗣️

Prøv å gjenskape dette bildet:

<figure>
    <img src="res/uv.png" alt="UV gradient" width=400>
    <figcaption><b>Hint:</b><i> Se hvilke farger som er i hjørnene av bildet</i></figcaption>
</figure>



### Løsningsforslag
<details>
<summary>Se Løsningsforslag</summary>

```glsl
void main(){
    vec2 st = (2. * uv - 1.) * vec2(u_resolution.x / u_resolution.y, 1.);
    vec2 mouse = u_mouse.xy / u_resolution;

    vec3 col = vec3(uv,0);

    out_color = vec4(
        col,
        1.
    );
}
```
</details>

## Oppgave 1.3: Miksing av farger
Nå skal vi introdusere en innebygd funksjon i GLSL [mix()](https://registry.khronos.org/OpenGL-Refpages/gl4/html/mix.xhtml). Denne tar inn 2 verdier(vektor/float) *a* og *b* og en float *t*, og gjør lineær interpolasjon mellom *a* og *b* basert på *t*. 

Så mix(0, 50, 0.5) = 25, siden 25 er midtpunktet mellom 0 og 50

Definer valgfrie farger (*f.eks. `vec3(1,0,1)` og `vec3(0,1,1)`*).
Deretter bruk mix() til å gjøre at du får en stilig gradient av fargene dine fra venstre til høyre.

<details>
<summary>Se Løsningsforslag</summary>

```glsl
void main(){
    vec3 magenta = vec3(1,0,1);
    vec3 cyan = vec3(0,1,1);
    
    vec3 col = mix(magenta,cyan,uv.x);

    out_color = vec4(
        col,
        1.
    );
}
```
</details>

## Oppgave 1.4: Bilder
<!-- TODO fiks oppgave tekst  -->
Nå skal sample en texture inn i shaderen vår.
Først må vi velge et bilde å laste inn

Trykk på Textures over editoren din, her kan du legge inn et bilde du ønsker å bruke. som f.eks. dette flotte bildet av verdens beste by:
<figure>
    <img src="res/bergen.jpg" alt="Smoothstep" width=600>
    <figcaption><i>Shaderen din blir 1000 ganger bedre med så flott bilde!</i></figcaption>
</figure>

Nå kan vi sample bildet inn i shaderen ved å bruke [texture()](https://registry.khronos.org/OpenGL-Refpages/gl4/html/texture.xhtml)
hvor `u_textures` er sampleren vår.

<details>
<summary>Se Løsningsforslag</summary>

```glsl
void main(){
    vec3 col = texture(u_textures[0], uv).rgb;

    out_color = vec4(
        col,
        1.
    );
}
```
</details>

# Del 2: Matematisk fargelegging 🧠
Nå skal vi gå over litt mer avanserte konsepter

## Oppgave 2.1: Sirkel
Nå skal vi tegne en sirkel på skjermen ved hjelp av litt matematikk 🤓

Vi vet jo at distansen mellom et punkt og en sirkel er 
```glsl
float circleDist(vec2 uv, vec2 center, float radius){
    return length(center-uv) - radius;
}
```
Hvor negative verdier vil si at punktet våres er inni sirkelen. Dette er en [Signed Distance Function](https://en.wikipedia.org/wiki/Signed_distance_function), som er brukt mye i shaderprogrammering.

Hvis du bruker denne distansen til sirkelen din, vil du få en ganske blurry sirkel. Det kan vi ikke ha noe av! 😡

Den enkle måten å fikse dette er en med vanlig *if/else* logikk. Dette vil gi deg en superskarp kant på sirkelen din, men her vil du mulig møte på litt [aliasing](https://en.wikipedia.org/wiki/Aliasing), altså at den blir litt pikselert-ish.

Men om du vil ha det litt penere, ved å kontrollere hvor blurry/skarp kanten din er, kan du bruke [smoothstep()](https://docs.gl/sl4/smoothstep) funksjonen i steden for *if/else*. Denne tar inn to grenseverdier, og en kildeverdi x. funksjonen gjør alle x-verdier mindre enn nedre grense til 0, og alle x-verdier over øvre grense til 1. x-verdier innenfor grensene, vil smoothly interpoleres mellom 0 og 1.

<figure>
    <img src="res/smoothstep.png" alt="Smoothstep" width=500>
    <figcaption><i>Smoothstep funksjon hvor grenseveridene er 0 og 1</i></figcaption>
</figure>


<details>
<summary>Se Løsningsforslag</summary>

```glsl
float circleDist(vec2 uv, vec2 center, float radius){
    return length(center-uv) - radius;
}

void main(){
    vec2 pos = vec2(0.5);
    
    float radius = 0.2;
    
    float dist = circleDist(uv,pos,radius);

    vec3 col = vec3(smoothstep(.0,.0001,dist));

    out_color = vec4(
        col,
        1.
    );
}
```
</details>

## Oppgave 2.2: Squiggly Sirkel
Nå som du har en fin sirkel på skjermen din, kan du jo ha det litt gøy med den.

Om du endrer på radius variabelen til noe mer dynamisk, kan du gjøre mye artig.

Hva om du vil ha en ruglete sirkel? Da kan du bruke vinkelen mellom senter av sirkelen og uv vektoren din
<figure>
    <img src="res/squiggly.png" alt="Squiggle Circle" width=400>
    <figcaption>Dette er det jeg mener med en <i>Ruglete Sirkel</i></figcaption>
</figure>

Her er en hjelpe funksjon jeg har laget for deg (Takk Tines!), den regner ut vinkelen for deg.
```glsl
float angleBetween(vec2 uv, vec2 pos){
    vec2 relPos = uv-pos;
    float angle = atan(relPos.y, relPos.x);
    return angle;
}
```
Denne verdien for seg selv kommer nok ikke til å vise noe super nyttig. Du kan derfor f.eks. bruke `sin()` til å gjøre den mer bølgete.

> NB: du kommer nok til å måtte skalere verdien din ned, enkel multiplisering med et tall mindre enn 1 vil holde 👍



<details>
<summary>Se Løsningsforslag</summary>

```glsl
float angleBetween(vec2 uv, vec2 pos){
    vec2 relPos = uv-pos;
    float angle = atan(relPos.y, relPos.x);
    return angle;
}

float circleDist(vec2 uv, vec2 center, float radius){
    return length(center-uv) - radius;
}

void main(){
    vec2 pos = vec2(0.5);
    
    float squiggleFrequency = 12.0;
    float squigglyAmplitude = 0.05;
    
    float angle = angleBetween(uv,pos);
    
    float squiggly = squigglyAmplitude * sin(angle*squiggleFrequency);
    
    float radius = 0.2 + squiggly;
    
    
    float dist = circleDist(uv,pos,radius);
    
    float thresh = smoothstep(.0, .1, dist);

    vec3 col1 = vec3(1,0,1);
    vec3 col2 = vec3(0,1,1);

    vec3 col = mix(col1,col2,thresh);

    out_color = vec4(
        col,
        1.
    );
}
```
</details>

# Del -1: Kreativitetens hjørne ✨
## Oppgave ∞: DIY
Nå er du ferdig med alle oppgavene, men du kan fortsatt gjøre mer! 🎉
Fikk noen av disse oppgavene hjernen din til å tenke på en kul tanke? Lag det da vell!

Du kan for eksempel bruke `u_time` variabelen som GLSL.app gir deg. Det er en float som sier hvor langt tid shaderen din har kjørt, i sekunder.

Hvis du er litt lost for inspirasjon, så er det alltid gøy å putte inn f.eks. en `sin()` funksjon på et litt tilfeldig sted og se hva som skjer

Hvis du trenger en `random` så finnes ikke det som en innbygget funksjon i GLSL, *men* du kan bruke en noise texture for random, slik som dette:

<figure>
    <img src="res/noise.png" alt="Noise Texture" width=400>
    <figcaption><i>Noise texture, hvor hver pixel er mellom 0-1</i></figcaption>
</figure>


## Resurser
[*Signed Distance Functions*](https://iquilezles.org/articles/distfunctions2d/): Liste med masse ulike signed distance functions som du kan bruke

[*Noise Texture Generator*](https://www.noisetexturegenerator.com/): Lar deg lage litt mer avansert noise textures

## Eksempler
[Her er en liten liste med shaders jeg har laget på fritiden](EKSEMPLER.md)