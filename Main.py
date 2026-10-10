from manim import *
import numpy as np

class GeburtstagMikroskop(MovingCameraScene):
    def construct(self):
        # Background-Farbe dunkel für schönen Kontrast
        self.camera.background_color = "#0f172a"

        # --------------------------------------------------
        # 1. OBJEKTE ERSTELLEN
        # --------------------------------------------------
        
        # Text am Anfang
        titel = Text("Alles Gute zum 24.!", font_size=40, color=TEAL_A)
        
        # Mikroskop (aus geometric VMobjects gebaut, damit Transformationen flüssig sind)
        fuß = RoundedRectangle(corner_radius=0.2, height=0.4, width=2.5, color=GREY, fill_opacity=0.8)
        arm = Line(start=[0.8, -1.2, 0], end=[0.5, 1.0, 0], color=LIGHT_GREY, stroke_width=8)
        tisch = Line(start=[-0.8, -0.3, 0], end=[0.8, -0.3, 0], color=GREY_A, stroke_width=5)
        
        # Tubus & Linse/Okular (das Zoom-Ziel)
        tubus = Rectangle(height=1.2, width=0.4, color=WHITE, fill_opacity=0.9).move_to([0, 0.8, 0])
        linse = Circle(radius=0.3, color=BLUE_B, fill_opacity=0.5).move_to([0, 1.5, 0])
        
        mikroskop = VGroup(fuß, arm, tisch, tubus, linse).move_to(ORIGIN)

        # Biologische Zelle (liegt genau hinter der Linse als Zoom-Ziel)
        zellwand = Circle(radius=1.8, color=GREEN_C, fill_opacity=0.2, stroke_width=3)
        zellkern = Dot(radius=0.4, color=PURPLE_B)
        zellkern_ring = DashedVMobject(Circle(radius=0.6, color=PURPLE_A))
        
        # Kleine Zell-Organellen (Mitochondrien / Bläschen)
        m1 = Dot(radius=0.1, color=YELLOW).move_to([0.8, 0.5, 0])
        m2 = Dot(radius=0.08, color=TEAL).move_to([-0.7, -0.6, 0])
        m3 = Dot(radius=0.12, color=RED_B).move_to([-0.9, 0.4, 0])
        
        zelle = VGroup(zellwand, zellkern, zellkern_ring, m1, m2, m3).move_to(linse.get_center())

        # Finaler Gruß für die Pathologie / Life Sciences
        untertext = Text("Life Sciences 2025", font_size=28, color=GOLD)
        untertext.next_to(zellwand, DOWN, buff=0.5)

        # --------------------------------------------------
        # 2. ANIMATIONS-ABLAUF
        # --------------------------------------------------

        # Schritt 1: Text "Alles Gute zum 24.!" schreiben (~1.5s)
        self.play(Write(titel), run_time=1.5)
        self.wait(0.5)

        # Schritt 2: Text morpht nahtlos in das Mikroskop (~2s)
        self.play(ReplacementTransform(titel, mikroskop), run_time=2)
        self.wait(0.5)

        # Schritt 3: KAMERA-ZOOM in die Linse des Mikroskops (~2s)
        # Die Kamera zoomt direkt auf das Zentrum der Linse
        self.play(
            self.camera.frame.animate.set(width=3).move_to(linse.get_center()),
            FadeIn(zelle, run_time=1.5),
            run_time=2
        )

        # Schritt 4: Zelle wird leicht größer & Wunschtext erscheint (~1.5s)
        self.play(
            self.camera.frame.animate.set(width=5).move_to(zelle.get_center()),
            FadeIn(untertext, shift=UP),
            run_time=1.5
        )

        # Schritt 5: Sanfte Pause am Ende fürs GIF-Looping (~2s)
        self.wait(2)