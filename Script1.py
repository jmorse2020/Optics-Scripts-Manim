#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:15:14 2023

@author: jackmorse
"""

from manim import *

class ElectromagneticWaveScene(ThreeDScene):
    def construct(self):
        """ Setting Up Axes """
        self.camera.background_color = DARKER_GREY
        self.set_camera_orientation(phi=2*PI/5, theta=(1.8)*PI/5 + PI)
        axes = ThreeDAxes(
            x_range=(-1, 10, 1), y_range=(- 5, 5, 1), z_range=(- 4, 4, 1), x_length=11, y_length=10, z_length=8
        )
        labels = axes.get_axis_labels()
        self.add(axes, labels)
        axes.scale(0.8)

        """ Defining the First EM Wave """
        lineFrequency = 0.2
        fieldDomain = (0, 10)
        electricField = ParametricFunction(lambda t: [t, 0, 2 * np.sin(t)], t_range=fieldDomain, color=ORANGE)
        electricFieldLines = VGroup(  *[Line([lineFrequency*i,0,0], [lineFrequency*i , 0, 2*np.sin(lineFrequency*i)], color = ORANGE)    for i in range(int(max(fieldDomain) / lineFrequency) + 1 ) ] ) 
        electricFieldLines.shift(axes.get_origin())
        electricField.shift(axes.get_origin())
        magneticField = ParametricFunction(lambda t: [t, 2 * np.sin(t), 0], t_range=fieldDomain, color=RED)
        magneticField.shift(axes.get_origin())
        magneticFieldLines = VGroup(  *[Line(start=[lineFrequency*j, 0, 0], end=[lineFrequency*j, 2*np.sin(lineFrequency*j), 0], color = RED)    for j in range(int(max(fieldDomain) / lineFrequency) + 1 ) ] ) 
        magneticFieldLines.shift(axes.get_origin())

        """ Add the wave to the scene """
        self.play(Create(electricField), Create(electricFieldLines), Create(magneticField), Create(magneticFieldLines), run_time = 1)
        # self.begin_ambient_camera_rotation(rate = 0.1)
        

        """ Move the wave """
        translationDistance = 0.1
        numberOfFrames = 100

        for i in range(1, numberOfFrames):
            self.set_camera_orientation(phi=2*PI/5, theta =(1.8)*PI/5 + PI + (i/numberOfFrames)  * PI / 6)
            newElectricField = ParametricFunction(lambda t: [t, 0, 2 * np.sin(t - i * translationDistance)], t_range=(0, 10), color=ORANGE)
            newElectricField.shift(axes.get_origin())
            newElectricFieldLines = VGroup(  *[Line(start=[lineFrequency*j, 0, 0], end=[lineFrequency*j, 0, 2*np.sin(lineFrequency*j - i * translationDistance)], color = ORANGE)    for j in range(int(max(fieldDomain) / lineFrequency) + 1 ) ] ) 
            newElectricFieldLines.shift(axes.get_origin())
            newMagneticField = ParametricFunction(lambda t: [t, 2 * np.sin(t - i * translationDistance), 0], t_range=(0, 10), color=RED)
            newMagneticField.shift(axes.get_origin())
            newMagneticFieldLines = VGroup(  *[Line(start=[lineFrequency*j, 0, 0], end=[lineFrequency*j, 2*np.sin(lineFrequency*j - i * translationDistance), 0], color = RED)    for j in range(int(max(fieldDomain) / lineFrequency) + 1 ) ] ) 
            newMagneticFieldLines.shift(axes.get_origin())
            self.play(Transform(electricField, newElectricField), Transform(electricFieldLines, newElectricFieldLines), Transform(magneticField, newMagneticField), Transform(magneticFieldLines, newMagneticFieldLines), run_time = 0.01)
           

        self.wait()
        return super().construct()

class UnpolarisedLight(ThreeDScene):
    def construct(self):
        import sys
        sys.setrecursionlimit(1500) 
        """ Setting Up Axes """
        self.camera.background_color = DARKER_GREY
        self.set_camera_orientation(phi=2*PI/5, theta=(1.8)*PI/5 + PI)
        axes = ThreeDAxes(
            x_range=(-1, 10, 1), y_range=(- 5, 5, 1), z_range=(- 4, 4, 1), x_length=11, y_length=10, z_length=8
        )
        labels = axes.get_axis_labels()
        self.add(axes, labels)
        axes.scale(0.8)

        """ Defining the EM Waves """  

        """ Wave 1"""        
        lineFrequency = 0.2
        fieldDomain = (0, 10)
        
        EMWave = LinearEMWave()        
        electricField_1_lambda = EMWave.electricField(angle=90*DEGREES)
        electricField_2_lambda = EMWave.electricField()
        # electricFieldLines = EMWave.electricFieldLines()
        electricField_1 = ParametricFunction(lambda t: electricField_1_lambda(t ,0), t_range=(0,10), color=ORANGE)
        electricField_1.shift(axes.get_origin())
        electricField_2 = ParametricFunction(lambda t: electricField_2_lambda(t ,0), t_range=(0,10), color=ORANGE)
        electricField_2.shift(axes.get_origin())
        print(electricField_1_lambda(1, 0))
        electricField_arr = []
        electricField_arr_lambda = []
        
        for i in range(0,3):
            random_angle = random.randint(0,360)
            print(random_angle)
            electricField_arr_lambda.append(EMWave.electricField(angle=random_angle*DEGREES))
            electricField_arr.append(ParametricFunction(lambda t: EMWave.electricField(angle=random_angle*DEGREES)(t ,0), t_range=(0,10), color=ORANGE).shift(axes.get_origin()))
            self.play(Create(electricField_arr[i]))
            
        electricField_arr_lambda_sum = lambda t: [0,0,0]
        # for i in range(0,2):
        print(type(electricField_arr_lambda_sum))
        print((electricField_arr_lambda[1](0, 0)))
        sum_lambda = lambda t: [sum(element) for element in zip(*(func(t, 0) for func in electricField_arr_lambda))]

        # sum_lambda = lambda t: [sum(f(t, 0)) for f in electricField_arr_lambda]
        print((sum_lambda))
        print(sum_lambda(0))
        self.play(Create(ParametricFunction(lambda t: sum_lambda(t), t_range = (0, 10), color = RED).shift(axes.get_origin())))
        # electricField_arr_lambda_sum_temp = lambda t: [x + y for x, y in zip(electricField_arr_lambda_sum(t), electricField_arr_lambda[0](t, 0))]
        # del electricField_arr_lambda_sum
        # print(type((electricField_arr_lambda_sum_temp)))
        # electricField_arr_lambda_sum = electricField_arr_lambda_sum_temp

        self.play(Create(ParametricFunction(lambda t: (electricField_arr_lambda_sum(t)), t_range=(0,10), color=ORANGE).shift(axes.get_origin())))
        self.wait()
        # print(type(electricField_1_lambda + electricField_2_lambda))
        # print(type(lambda t: sum(x) for x in zip(electricField_2_lambda(t, 0 ), electricField_1_lambda(t, 0))))
        # add_functions = lambda x: lambda y: x(y) + z(y)
        electricField_sum_lambda = lambda t: [x + y for x, y in zip(electricField_1_lambda(t ,0), electricField_2_lambda(t,0))]
        print(electricField_sum_lambda(1))
        electricField_sum = ParametricFunction(lambda t: electricField_sum_lambda(t), t_range=(0,10), color=ORANGE)
        electricField_sum.shift(axes.get_origin())

        self.play(Create(electricField_1), Create(electricField_2), run_time = 1)
        self.wait(0.5)
        
        self.play(Transform(electricField_1, electricField_sum), Transform(electricField_2, electricField_sum))
        # self.remove(electricField_sum)
        self.wait()

        # electricFieldLines = VGroup(  *[Line(start=electricFieldLines[0][i], end=electricFieldLines[1][i], color = ORANGE) for i in range(0, len(electricFieldLines[1]) - 1)])
        # electricFieldLines.shift(axes.get_origin())



class Scene_1_Introduction(Scene):
    def construct(self):
        title = Text("Understaning Polarisation and Malus' Law")
        self.play(Write(title))


class Video(Scene):
    def construct(self):
        Scene_1_Introduction().render()