#!/bin/env python3
import numpy as np
from manim import *


def formel_mathtex(index: str):
    return MathTex(
        "d_", "{" + index + "}", "=", "1", "+", r"( {{ D }} - {{ k }} ) ", r"\cdot \left(", r"\frac{1}{2}",
        r"{\mathrm{JL}_{ {{ " + index + r" }} } \over \mathrm{JL}_\mathrm{gesamt}", "}+", r"\frac{1}{2}",
        r"{ \sqrt{M_{ {{ " + index + r" }} } } \over \sum_{i=1}^k \sqrt{M_i} }", r"\right)"
    )

JL_FORMEL_TEX = r"{ {{\mathrm{JL}_n }} \over {{ \mathrm{JL}_\mathrm{gesamt} }} }"
JL_FORMEL_SHIFT = LEFT * 3

M_FORMEL_TEX = r"{ {{ \sqrt{M_n} }} \over {{ \sum }} _{i=1}^k {{ \sqrt{M_i} }} }"
M_FORMEL_SHIFT = LEFT * 3


def print_formular_parts(formular: MathTex):
    for i, ss in enumerate(formular):
        print(i, ss)


class TimedScene(Scene):

    def __init__(self, renderer=None, camera_class=Camera, always_update_mobjects=False, random_seed=None,
                 skip_animations=False, debug_time=False):
        self.video_time = 0
        self.debug_time = debug_time
        if self.debug_time:
            self.timing_test = Text("test")
        super().__init__(renderer, camera_class, always_update_mobjects, random_seed, skip_animations)

    def play(self, *args, **kwargs):
        if "run_time" not in kwargs:
            kwargs["run_time"] = 1
        self.update_timing_display()
        #self.video_time += self.get_run_time(args)
        #print(self.get_run_time(args), len(args))
        self.video_time += kwargs["run_time"]
        super().play(*args, **kwargs)
        self.update_timing_display()

    def wait_until_timestamp(self, timestamp: int):
        if self.video_time > timestamp:
            print(f"Warning, video is rushing away, {self.video_time - timestamp} seconds")
        else:
            self.wait(timestamp - self.video_time)

    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None):
        self.play(Wait(run_time=duration, stop_condition=stop_condition), run_time=duration)

    def update_timing_display(self):
        if self.debug_time:
            self.remove(self.timing_test)
            self.timing_test = Text(str(self.video_time))
            self.timing_test.shift(DOWN*2)
            self.add(self.timing_test)


class Scene0(TimedScene):

    def construct(self):
        formel_normal = Tex("F", "o", "r", "m", "e", "l", font_size=150).shift(DOWN)
        formel_math = Tex(r"$\Gamma$", r"$\sigma$", "i", r"$\omega$",
                r"$e$", r"$\lfloor$", font_size=150).shift(DOWN)
        formel_normal = Tex("Formel", font_size=150).shift(DOWN)
        formel_math = Tex(r"$\Gamma$$\sigma$i$\omega$$e$$\lfloor$", font_size=150).shift(DOWN)
        upper_title = Text("Offenes Delegiertensystem in der JDAV").shift(UP * 2)
        pre_title = Text("Erklärung zur", font_size=30)
        post_title = Text("mit der die Anzahl der Delegierten pro Sektion berechnet wird", font_size=30).shift(DOWN * 2.2)
        # subtitle = Text("Erklärung der Formel zur Berechnung der Delegiertenanzahl pro Sektion", font_size=30).shift(DOWN)
        # subtitle = Text("Erklärung zur Formel mit der die Anzahl der Delegierten pro Sektion berechnet wird", font_size=30).shift(DOWN)
        self.add(upper_title)
        self.play(Write(formel_math, run_time=1), run_time=1)
        self.play(
                Transform(formel_math, formel_normal, run_time=1),
                FadeIn(pre_title, run_time=1),
                FadeIn(post_title, run_time=1)
                , run_time=1)
        self.wait(2)
        self.play(FadeOut(upper_title, pre_title, post_title, formel_math))


class Scene1(TimedScene):
    def construct(self):

        # Index Erklaerung

        formel_index_examples = [formel_mathtex(x) for x in ["n", r"\text{Jena}", r"\text{Ulm}", "n"]]
        self.play(Write(formel_index_examples[0]), run_time=4)
        # self.add(formel_index_examples[0])

        info_text_1 = Text("Laut BJA Antrag zum BJLT 2021", font_size=20)
        info_text_2 = Text("Mathematisch Äquivalent zum Beschluss des a.o. BJLT 2020", font_size=20)
        info_text_1.shift(DOWN * 3)
        info_text_2.shift(DOWN * 3.3)
        self.play(FadeIn(info_text_1), FadeIn(info_text_2))

        print_formular_parts(formel_index_examples[0])

        index_boxes = [
            SurroundingRectangle(Group(formel_index_examples[0][0], formel_index_examples[0][1])),
            SurroundingRectangle(Group(*formel_index_examples[0][12:14])),
            SurroundingRectangle(Group(*formel_index_examples[0][17:19])),
        ]
        self.wait_until_timestamp(14)
        self.play(Create(index_boxes[0]),
                  FadeOut(info_text_1), FadeOut(info_text_2))
        self.wait_until_timestamp(20)
        for index_box in index_boxes[1:]:
            self.play(Create(index_box))
        self.wait_until_timestamp(24)

        self.play(FadeOut(*index_boxes))

        self.wait_until_timestamp(25)
        for i in range(len(formel_index_examples) - 1):
            self.play(ReplacementTransform(formel_index_examples[i], formel_index_examples[i + 1]))
            self.wait(1)
        formel = formel_index_examples[-1]

        # Erklaerung der Teile

        ## Aufteilung

        self.wait_until_timestamp(31)
        self.play(Circumscribe(formel[3], fade_out=True))
        self.play(Circumscribe(Group(*formel[5:]), fade_out=True))

        ## Basisstimme

        self.wait_until_timestamp(33)
        base_vote_box = SurroundingRectangle(formel[3])
        base_vote_text = Text("Basisstimme")
        base_vote_text.set_color(YELLOW)
        base_vote_text.next_to(formel[3], DOWN)
        base_vote_text.shift(DOWN * 0.8)
        self.play(Create(base_vote_box))
        self.play(Write(base_vote_text))

        self.wait_until_timestamp(43)

        self.play(FadeOut(base_vote_box),
                  FadeOut(base_vote_text))

        self.wait_until_timestamp(45)
        self.play(Create(index_boxes[1]))
        self.play(Create(index_boxes[2]))
        self.wait_until_timestamp(48)
        self.remove(index_boxes[1])
        self.remove(index_boxes[2])

        ## Praefix (D-k)

        self.wait_until_timestamp(49)
        self.play(Circumscribe(Group(*formel[5:10])))

        self.wait_until_timestamp(54)
        D_text = Text("Zielgröße")
        D_text.next_to(formel[6], UP)
        D_text.shift(UP * 0.6)
        D_text.set_color(GREEN)

        self.play(
            Circumscribe(formel[6], color=GREEN),
            formel[6].animate.set_color(GREEN),
            Write(D_text)
        )
        self.wait()

        self.wait_until_timestamp(60)
        k_text = Text("Anzahl Sektionen")
        k_text.next_to(formel[8], DOWN)
        k_text.shift(DOWN * 0.6)
        k_text.set_color(RED)

        self.play(
            formel[8].animate.set_color(RED),
            Circumscribe(formel[8], color=RED),
            Write(k_text),
            run_time=1
        )
        self.wait_until_timestamp(75)

        self.play(FadeOut(D_text), FadeOut(k_text))
        formel[6].to_original_color()
        formel[8].to_original_color()

        ## Aufteilung in Haelften

        self.wait_until_timestamp(79)
        self.play(Circumscribe(Group(*formel[11:15]), fade_out=True))
        self.play(Circumscribe(Group(*formel[16:20]), fade_out=True))

        self.wait_until_timestamp(84)
        self.play(
            Indicate(formel[11]),
            Indicate(formel[16])
        )

        ## Uebergang zu JL Erklaerung

        self.wait_until_timestamp(88)
        jl_box = SurroundingRectangle(Group(*formel[12:15]))
        self.play(Create(jl_box))

        jl_formel = MathTex(JL_FORMEL_TEX)
        self.play(
            FadeOut(VGroup(*formel[:12])),
            FadeOut(VGroup(*formel[15:])),
            FadeOut(jl_box),
            # formel.animate.shift(LEFT * 3)
        )
        VGroup(*formel[:12]).set_opacity(0)
        VGroup(*formel[15:]).set_opacity(0)
        #self.play(formel.animate.shift(LEFT * 3))
        jl_formel.shift(JL_FORMEL_SHIFT)

        # JL Erklaerung

        self.play(FadeTransform(VGroup(*formel[12:15]), jl_formel))
        #self.remove(formel)
        #self.add(jl_formel)

        self.wait(1)


class Scene2(TimedScene):
    def construct(self):
        jl_formel = MathTex(JL_FORMEL_TEX)
        jl_formel.shift(JL_FORMEL_SHIFT)
        self.add(jl_formel)

        self.wait_until_timestamp(2)
        self.play(Circumscribe(jl_formel[1], fade_out=True))
        self.wait_until_timestamp(5)
        self.play(Circumscribe(jl_formel[3], fade_out=True))

        circle = Circle(1, color=RED)
        sector = AnnularSector(inner_radius=1, outer_radius=0, angle=0.5, start_angle=0.5, color=BLUE)
        circle.shift(RIGHT * 2)
        sector.shift(RIGHT * 2)

        self.wait_until_timestamp(13)
        self.play(
            FadeIn(sector, scale=0.2),
            Flash(jl_formel[1], color=BLUE, line_length=0.6),
            jl_formel[1].animate.set_color(BLUE)
        )
        self.wait_until_timestamp(16)
        self.play(
            Create(circle),
            Circumscribe(jl_formel[3], color=RED),
            jl_formel[3].animate.set_color(RED)
        )
        self.wait(1)

        self.wait_until_timestamp(32)

        self.play(
            FadeOut(circle),
            FadeOut(sector),
            jl_formel.animate.set_color(WHITE)
        )

        dots_origin = ORIGIN + UP * 1 + RIGHT
        spacing = 0.8
        rows = 4
        colors = [GREEN, YELLOW, RED, BLUE]
        dots = [VGroup(*[Dot(dots_origin + RIGHT * spacing * ii + DOWN * spacing * i, radius=0.2, color=colors[i]) for ii in range(3)]) for i in range(rows)]
        timestamps = [40, 45, 47, 48]
        numbers = [Text(str(i + 1), color=colors[i]).shift(dots_origin + spacing * LEFT + spacing * DOWN * i) for i in range(rows)]

        self.wait_until_timestamp(36)
        label = Text("3").shift(dots_origin + spacing * RIGHT + spacing * UP)
        self.play(Write(label))

        for i in range(rows):
            self.wait_until_timestamp(timestamps[i])
            self.play(Write(numbers[i]),
                        ShowIncreasingSubsets(dots[i]))

        self.wait(1)

        self.play(FadeOut(label), *([FadeOut(d) for d in dots] + [FadeOut(n) for n in numbers]))

        self.wait(1)


class Scene3(TimedScene):
    def construct(self):

        # Uebergang von JL Formel zu M Formel

        jl_formel = MathTex(JL_FORMEL_TEX)
        jl_formel.shift(JL_FORMEL_SHIFT)
        self.add(jl_formel)
        formel = formel_mathtex("n")

        self.play(FadeTransform(jl_formel, VGroup(*formel[12:15])))
        self.play(
            FadeIn(VGroup(*formel[:12])),
            FadeIn(VGroup(*formel[15:])),
        )

        self.wait_until_timestamp(4)
        m_box = SurroundingRectangle(Group(*formel[17:20]))
        self.play(Create(m_box))

        m_formel = MathTex(M_FORMEL_TEX)
        self.play(
            FadeOut(VGroup(*formel[:17])),
            FadeOut(VGroup(*formel[20:])),
            FadeOut(m_box),
            # formel.animate.shift(LEFT * 3)
        )
        VGroup(*formel[:17]).set_opacity(0)
        VGroup(*formel[20:]).set_opacity(0)
        #self.play(formel.animate.shift(LEFT * 3))
        m_formel.shift(M_FORMEL_SHIFT)
        self.play(FadeTransform(VGroup(*formel[17:20]), m_formel))

        self.wait(1)


class Scene4(TimedScene):
    def construct(self):

        # M Formel Erklaerung

        m_formel = MathTex(M_FORMEL_TEX)
        m_formel.shift(M_FORMEL_SHIFT)
        self.add(m_formel)
        print_formular_parts(m_formel)

        ## Wurzel Erklaerung

        self.wait_until_timestamp(6)
        wurzel = MathTex(r"\sqrt{ {{ M_n }} }", r"=\sqrt{3^2} = 3")
        wurzel.shift(RIGHT * 1.5 + UP * 0.5)
        wurzel[-1].set_opacity(0)
        self.play(Write(wurzel))
        self.wait_until_timestamp(9)
        wurzel_3 = MathTex(r"\sqrt{ {{ 9 }} }", r"=\sqrt{3^2} = 3")
        wurzel_3.shift(RIGHT * 1.5 + UP * 0.5)
        self.play(Transform(wurzel, wurzel_3))

        quadrat = MathTex(r"9 = 3^2 = 3\cdot 3")
        quadrat.shift(RIGHT * 1.8 + DOWN * 0.5)
        self.play(Write(quadrat))

        self.wait_until_timestamp(27)

        self.play(
            FadeOut(wurzel),
            FadeOut(quadrat)
        )

        ## Summenerklaerung

        self.wait_until_timestamp(30)
        self.play(Circumscribe(m_formel[3], fade_out=True, run_time=3), run_time=3)

        summe = MathTex(r"{ {{ \sqrt{M_n} }} \over {{ }} {{ \sqrt{M_1} + \sqrt{M_2} + \sqrt{M_3} + \dots + \sqrt{M_k} }} }")
        summe[1].set_opacity(0)
        m_formel[1].set_opacity(0)

        m_formel_upper = MathTex(M_FORMEL_TEX)
        m_formel_upper.shift(M_FORMEL_SHIFT)
        m_formel_upper.set_opacity(0)
        m_formel_upper[1].set_opacity(1)
        self.add(m_formel_upper)

        self.wait_until_timestamp(36)
        m_formel_old = m_formel.copy()
        self.play(Transform(m_formel, summe))
        self.wait_until_timestamp(41)
        self.play(Transform(m_formel, m_formel_old))
        self.remove(m_formel_old)
        self.remove(m_formel_upper)
        self.remove(m_formel)
        m_formel = MathTex(M_FORMEL_TEX)
        m_formel.shift(M_FORMEL_SHIFT)
        self.add(m_formel)

        ## Anteil

        self.wait_until_timestamp(46)
        self.play(Circumscribe(m_formel[1], color=BLUE))
        self.wait_until_timestamp(48)
        self.play(Circumscribe(VGroup(*m_formel[3:6]), color=RED))

        # Graph

        self.wait_until_timestamp(52)

        ax = Axes(x_range=[1, 40, 1], y_range=[1, 40, 1], x_length=3, y_length=3, axis_config={"include_ticks": False}, tips=False).shift(RIGHT)
        linear_graph = ax.get_graph(lambda x: x, color=WHITE)
        linear_graph_2 = ax.get_graph(lambda x: x, color=WHITE).set_opacity(0.2)
        sqrt_graph = ax.get_graph(lambda x: np.sqrt(x) * 2, color=WHITE)
        x = MathTex("{{ x }}").next_to(linear_graph)
        x_wurzel = MathTex(r"\sqrt{ {{ x }} }").next_to(linear_graph)
        self.wait_until_timestamp(54)
        self.play(FadeIn(ax), Create(linear_graph), Create(linear_graph_2), Write(x))
        self.wait_until_timestamp(57)
        self.play(Transform(linear_graph, sqrt_graph), Transform(x, x_wurzel))
        self.wait_until_timestamp(60)
        self.remove(ax, linear_graph, linear_graph_2, sqrt_graph, x, x_wurzel)

        ## Quadrat

        self.wait_until_timestamp(63)

        dots_origin = ORIGIN + UP * 1 + RIGHT
        spacing = 0.8
        rows = 4
        colors = [GREEN, YELLOW, RED, BLUE]
        dots = []
        for i in range(rows):
            row = [Dot(dots_origin + RIGHT * spacing * ii + DOWN * spacing * i, color=colors[i]) for ii in range(i + 1)] + [Dot(dots_origin + RIGHT * spacing * i + DOWN * spacing * ii, color=colors[i]) for ii in reversed(range(i))]
            dots.append(VGroup(*row))
        numbers = [Text(str(i + 1), color=colors[i]).shift(dots_origin + spacing * LEFT + spacing * DOWN * i) for i in range(rows)]
        timestamps = [(82, 85, 85), (87, 89, 91), (94, 96, 98), (101, 101, 101)]

        dot_for_scale = Dot(dots_origin, color=WHITE)
        dot_scale = Tex(r"= 125 Mitglieder")
        dot_scale.shift(dots_origin + UP * spacing * 2 + RIGHT * spacing * 1.7)
        dot_for_scale.next_to(dot_scale, LEFT)
        self.play(
            Create(dot_for_scale),
            Write(dot_scale)
        )

        for i in range(rows):
            self.wait_until_timestamp(timestamps[i][0])
            self.play(Write(numbers[i]))
            self.wait_until_timestamp(timestamps[i][1])
            self.play(ShowIncreasingSubsets(dots[i]))
            self.wait_until_timestamp(timestamps[i][2])
            self.play(Circumscribe(dots[i], color=WHITE, buff=0.2, fade_out=True))

        self.wait_until_timestamp(110)

        self.play(
            VGroup(*dots).animate.set_opacity(0.2),
            FadeOut(VGroup(*numbers)),
            FadeOut(dot_scale),
            FadeOut(dot_for_scale),
        )
        quadrat_wurzel = MathTex(r"\sqrt{x^2} = x")
        quadrat_wurzel.next_to(VGroup(*dots), UP, buff=1.7)
        self.play(Write(quadrat_wurzel))

        self.wait_until_timestamp(112)
        quadrat = SurroundingRectangle(VGroup(*dots))
        x_1 = MathTex("x").next_to(quadrat, UP)
        x_2 = MathTex("x").next_to(quadrat, RIGHT)
        x__2 = MathTex("x^2").move_to(quadrat)
        self.play(Create(quadrat))
        self.play(Write(x_1), Write(x_2), Write(x__2))

        self.wait_until_timestamp(119)

        self.play(
            FadeOut(VGroup(*dots)),
            FadeOut(quadrat, x_1, x_2, x__2, quadrat_wurzel),
        )

        self.wait(1)


class Scene5(TimedScene):
    def construct(self):
        ## fade back to complete formular

        m_formel = MathTex(M_FORMEL_TEX)
        m_formel.shift(M_FORMEL_SHIFT)
        self.add(m_formel)

        formel = formel_mathtex("n")

        self.play(FadeTransform(m_formel, VGroup(*formel[17:20])))
        self.play(
            FadeIn(VGroup(*formel[:17])),
            FadeIn(VGroup(*formel[20:])),
        )

        # abschliessende Uebersicht

        self.wait_until_timestamp(5)
        self.play(Circumscribe(formel[:2], fade_out=True))
        self.wait_until_timestamp(7)
        formel_jena = formel_mathtex(r"\text{Jena}")
        self.play(ReplacementTransform(formel, formel_jena))

        self.wait_until_timestamp(12)
        self.play(Circumscribe(formel_jena[3], fade_out=True))
        self.wait_until_timestamp(15)
        self.play(Indicate(formel_jena[12:15]), Indicate(formel_jena[17:20]))
        self.wait_until_timestamp(18)
        rectangle = SurroundingRectangle(formel_jena[12:15])
        self.play(Create(rectangle))
        self.wait_until_timestamp(26)
        self.play(FadeOut(rectangle))
        #self.play(Circumscribe(formel_jena[12:15], fade_out=True))
        self.wait_until_timestamp(29)
        rectangle = SurroundingRectangle(formel[17:20])
        self.play(Create(rectangle))
        #self.play(Circumscribe(formel_jena[17:20], fade_out=True))
        self.wait_until_timestamp(35)
        self.play(FadeOut(rectangle))

        self.wait_until_timestamp(51)
        self.play(FadeOut(formel_jena))

        self.wait(1)


class Scene6(Scene):

    def construct(self):
        self.play(
            FadeIn(Text("Animationen mit Manim", font_size=20).shift(DOWN * 2.5)),
            FadeIn(Text("CC-BY-NC-SA 4.0 2021", font_size=20).shift(DOWN * 3)),
            FadeIn(Text("Für die Jugend des Deutschen Alpenvereins www.jdav.de", font_size=20).shift(DOWN * 3.5)),
            Write(Text("Jetzt Lust auf Mathe-Videos bekommen?", font_size=40).shift(UP * 0.3))
        )
        self.play(
            Write(Text("Dann wird dir 3Blue1Brown gefallen!", font_size=40).shift(DOWN * 0.7))
        )

        self.wait(5)
